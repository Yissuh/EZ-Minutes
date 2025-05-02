import sys
sys.stdout.reconfigure(encoding="utf-8")  # Force UTF-8 for all print statements
print("Processing")
#With try catch error handling working overall
from torch import device,cuda
import torch
import time 
from os.path import basename, splitext, join, exists
from os import environ, remove, makedirs, _exit,chdir
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
from re import sub
from polars import scan_csv,col, DataFrame
import torchaudio
import subprocess
import gc
from pathlib import Path
from intervaltree import IntervalTree

# Automatically select CUDA if available, otherwise use CPU
dev = device("cuda" if cuda.is_available() else "cpu")
device = str(dev)
compute_type = "float16" if device == "cuda" else "int8"
print(f"Using device: {device}")
# For extra file de letion
check_extract = False
check_convert = False
audio_output_path = ""

# Set environment variable for OpenMP
environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def main(file_path, min_speakers):
    # Get the absolute path of the script's directory
    script_dir = Path(__file__).parent
    global check_convert, check_extract
    # Start time tracking
    start_timer = time.time()

    file_name = basename(file_path)

    # Initialize Faster Whisper model
    model_size = "medium"

    # Check if the variable is a string
    if isinstance(device, str):
        print("The variable is a string!")
    else:
        print("The variable is not a string.")
        
    def is_audio_valid(file_path):
        try:
            torchaudio.load(file_path)
            return True
        except Exception as e:
            print(f"❌ Invalid audio file:\n{e}")
            return False
        
    # Load the words into a Polars DataFrame from the CSV file
    try:
        # Read the CSV file lazily
        tagalog_vocab = scan_csv("TagLish_vocab.csv", has_header=True)
        # Pre-load the vocabulary into a set for faster lookups
        vocab_words = set(tagalog_vocab.collect()["word"].to_list())
        print("Done loading tagalog vocab from CSV.")
    except Exception as e:
        print(f"Error loading the words from CSV: {e}")

    # Create translation table for punctuation
    punct_to_remove = "!\"#$%&()*+,./:;<=>?@[\\]^_`{|}~"
    translator = str.maketrans('', '', punct_to_remove)


    try:
        is_audio_valid(file_path)
        audio_output_path = splitext(file_path)[0] + '_preprocessed.wav'
        command = [
            "ffmpeg", "-y",
            "-i", file_path,
            "-vn",              # remove video stream
            "-ac", "1",         # mono channel
            "-ar", "16000",     # 16kHz sample rate
            "-acodec", "pcm_s16le",  # WAV 16-bit PCM format
            audio_output_path
        ]

        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Audio/Video converted successfully to '{audio_output_path}'")
    except Exception as e:
        print(f"Error during file conversion: {e}")
        
    file_path = audio_output_path

    # Initialize the Whisper model
    try:
        FasterWhisperPath= script_dir.parent / "models" / "models--Systran--faster-whisper-medium" / "snapshots" / "08e178d48790749d25932bbc082711ddcfdfbc4f"
        model = WhisperModel(str(FasterWhisperPath), device=device, compute_type=compute_type)
        print(f"Using Whisper model size: {model_size}")
    except Exception as e:
        print(f"Error initializing Whisper model: {e}")

    # Transcribe the audio file
    try:
        # Define your init prompt
        init_prompt = "hmm, hmmp, um, uhh, huh, ano, like, kasi, and, well, weh, parang"

        vad_parameters = dict(
        threshold=0,
        min_speech_duration_ms=300,
        max_speech_duration_s=25,
        speech_pad_ms=50
    )
        
        segments, info = model.transcribe(file_path, beam_size=5, initial_prompt=init_prompt,
                                        vad_filter=True, vad_parameters=vad_parameters, 
                                        word_timestamps=True, )
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    except Exception as e:
        print(f"Error during transcription: {e}")

    # Initialize pyannote speaker diarization
    try:
        # Construct the absolute path to config.yaml
        config_path = script_dir.parent / "models" / "pyannote_diarization_config.yaml" / "config.yaml"
        offline_diarization = Pipeline.from_pretrained(config_path)
        offline_diarization.to(dev)

        diarization = offline_diarization(file_path, min_speakers=min_speakers)
        print("Diarization Successful")
    except Exception as e:
        print(f"Error during diarization: {e}")

    # Initialize output_text to an empty string at the start
    output_text = ""

    try:
        # Step 1: Build the IntervalTree for speaker segments
        speaker_segments = []
        speaker_mapping = {}
        speaker_index = 0
        interval_tree = IntervalTree()  # Initialize the IntervalTree

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if speaker not in speaker_mapping:
                speaker_mapping[speaker] = f"SPEAKER {speaker_index}"
                speaker_index += 1
            
            speaker_segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker_mapping[speaker]
            })
            
            # Add speaker intervals to the IntervalTree
            interval_tree[turn.start:turn.end] = speaker_mapping[speaker]

        print("Speaker segments indexed into IntervalTree")

        # Step 2: Group words into sentences with the interval tree
        buffer = 0
        sentence_data = []
        current_sentence = []
        current_speaker = None
        sentence_start = None
        end_markers = {'.', '?', '!'}

        try:
            for segment in segments:
                for word_info in segment.words:
                    word_start = word_info.start
                    word_end = word_info.end
                    word_text = word_info.word.strip()

                    if not word_text:
                        continue

                    # Use the IntervalTree to find the matching speaker for the word
                    try:
                        matching_speakers = interval_tree.overlap(word_start, word_end)  # Use overlap instead of pop
                        if matching_speakers:
                            speaker = matching_speakers.pop().data  # Extract speaker
                        else:
                            speaker = "UNKNOWN"
                    except Exception as e:
                        print(f"Error in finding speaker for word: {e}")
                        speaker = "UNKNOWN"

                    if sentence_start is None:
                        sentence_start = word_start
                        current_speaker = speaker

                    current_sentence.append(word_text)

                    ends_sentence = any(word_text.endswith(marker) for marker in end_markers)

                    if ends_sentence or speaker != current_speaker:
                        sentence_text = ' '.join(current_sentence)
                        sentence_text = sub(r'\s+([.,!?])', r'\1', sentence_text)

                        sentence_data.append({
                            'start': sentence_start,
                            'end': word_end,
                            'speaker': current_speaker,
                            'text': sentence_text
                        })

                        current_sentence = []
                        sentence_start = None if ends_sentence else word_end
                        current_speaker = speaker

            # Handle any remaining sentence
            if current_sentence:
                sentence_text = ' '.join(current_sentence)
                sentence_text = sub(r'\s+([.,!?])', r'\1', sentence_text)
                sentence_data.append({
                    'start': sentence_start,
                    'end': word_end,
                    'speaker': current_speaker,
                    'text': sentence_text
                })

            sentences_df = DataFrame(sentence_data).lazy()
            sentences_df = sentences_df.collect()  # Collect results
            print("Done Grouping and Identifying Sentences")

        except Exception as e:
            print(f"Error grouping words into sentences: {e}")
            sentences_df = DataFrame(columns=['start', 'end', 'speaker', 'text']).lazy()

        # Step 3: Process the sentences and highlight vocabulary words
        try:
            speaker_map = {}
            speaker_count = 0
            previous_speaker = None
            current_texts = []
            start_time = None
            end_time = None
            unknown_buffer = []  # Store UNKNOWN words temporarily

            output_text = ""  # Initialize output text

            for row in sentences_df.iter_rows():
                start_time_current = f"{row[0]:.2f}"
                end_time_current = f"{row[1]:.2f}"
                speaker = row[2]
                text = row[3]

                # Process text highlighting
                try:
                    text = sub(r'\s*-\s*', '-', text)  # Remove spaces around hyphens
                    words = [word.translate(translator).lower() for word in text.split()]
                    original_words = text.split()

                    # Highlight words based on vocabulary
                    highlighted_words = []
                    for orig, cleaned in zip(original_words, words):
                        if ("'" in cleaned and cleaned.endswith("s")) or '-' in cleaned or cleaned in vocab_words:
                            highlighted_words.append(orig)
                        else:
                            highlighted_words.append(f"({orig})")

                    processed_text = ' '.join(highlighted_words)
                except Exception as e:
                    print(f"Error highlighting words: {e}")
                    processed_text = text

                # Handle speaker mapping
                if speaker != "UNKNOWN":
                    if speaker not in speaker_map:
                        speaker_map[speaker] = speaker_count
                        speaker_count += 1
                    current_speaker = f"SPEAKER {speaker_map[speaker]}"
                else:
                    current_speaker = "UNKNOWN"

                # Merge UNKNOWN words with previous speaker if alternating
                if current_speaker == "UNKNOWN":
                    unknown_buffer.append(processed_text)  # Store UNKNOWN words
                    continue  # Skip adding UNKNOWN as a separate speaker

                # If there were UNKNOWN words before this speaker, merge them
                if unknown_buffer:
                    processed_text = " ".join(unknown_buffer) + " " + processed_text
                    unknown_buffer = []  # Clear buffer after merging

                # If speaker changes, save previous text block
                if current_speaker != previous_speaker and previous_speaker is not None:
                    combined_text = ' '.join(current_texts)
                    output_text += f"[{start_time} - {end_time}] {previous_speaker}: {combined_text}\n"
                    current_texts = []
                    start_time = None

                # Start a new text block for a new speaker
                if start_time is None:
                    start_time = start_time_current
                end_time = end_time_current
                current_texts.append(processed_text)
                previous_speaker = current_speaker

            # Handle last speaker block
            if current_texts:
                combined_text = ' '.join(current_texts)
                output_text += f"[{start_time} - {end_time}] {previous_speaker}: {combined_text}\n"

            print("Done merging UNKNOWN words into speakers.")

        except Exception as e:
            print(f"Error during output processing: {e}")
            output_text = ""  # Ensure output_text is initialized even on failure

    except Exception as e:
        print(f"Error during the entire process: {e}")
        output_text = ""  # Ensure output_text is initialized even on failure

    print(output_text)

        
    # Save the output_text to a text file   
    folder_outputs = "outputs"
    makedirs(folder_outputs, exist_ok=True)
    output_file_path = join(folder_outputs, file_name + ".txt")
    
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(output_text)

    # Remove temporary files if needed
    try:
        if exists(audio_output_path):
            remove(audio_output_path)
            print(f"Removed temporary file '{audio_output_path}'")
    except Exception as e:
        print(f"Error removing temporary files: {e}")
        
    sys.stdout.flush()  # Flush print buffer (important!)
    gc.collect()
    torch.cuda.empty_cache()
        
    # Calculate and print execution time
    end_timer = time.time()
    elapsed_timer = end_timer - start_timer
    elapsed_minutes = elapsed_timer / 60
    elapsed_hours = elapsed_timer / 3600

    print(f"Total runtime: {elapsed_timer:.2f} second/s")
    print(f"Total runtime: {elapsed_minutes:.2f} minute/s")
    print(f"Total runtime: {elapsed_hours:.2f} hr/s")
    
    print("Whole Process Completed")
    _exit(0)


try:
    if __name__ == "__main__":
        if len(sys.argv) < 3:
            print("Error: Missing arguments. Usage: python DiarizedTranscription.py <file_path> <min_speakers>")
            sys.exit(1)  # Exit with an error

        file_path = sys.argv[1]  # Get first argument (audio file path)
        min_speakers = int(sys.argv[2])  # Convert second argument to an integer

        main(file_path, min_speakers)  # Call main() with extracted arguments
    # if __name__ == "__main__":
    #     output=main("C:/Users/joech/Desktop/Transcription/Audios/ariana filler.mp3", 2)
    #     #C:/Users/joech/Desktop/4thYear1stSem/Audios Unused
except Exception as e:
        print(f"Error has occured: {e}")

finally:
    print("Whole Process Completed")