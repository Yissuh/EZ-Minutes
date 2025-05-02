import time
# **Start Timer**
start_time = time.time()
import torch
import re
from transformers import NllbTokenizer,AutoModelForSeq2SeqLM  # Change AutoTokenizer to NllbTokenizer
from torch.amp import autocast  # Import from torch.amp instead of torch.cuda.amp
from pathlib import Path
from os import makedirs, _exit,remove
from os.path import join, basename,exists
import sys
from database import (
    init_db, save_meeting, get_all_recordings,
    get_meeting_by_id, delete_meeting_by_id
)

def main(meeting_id,file_name):
    script_dir = Path(__file__).parent
    
    folders_outputs = "translations"
    makedirs(folders_outputs, exist_ok=True)
    outputs_file_path = join(script_dir, folders_outputs, "translated_"+ file_name + ".txt")

    if exists(outputs_file_path):
        remove(outputs_file_path)
    
    meeting_id= int(meeting_id)
    
    file_name, title, agenda, transcript, is_translated, translated_transcript , minutes = get_meeting_by_id(meeting_id)
    
    transcript = str(transcript)
    
    match = re.search(r"Meeting Transcript:(.*)", transcript, re.DOTALL)
    rematch = re.search(r"(Meeting Date:.*?Meeting Transcript:)",transcript, re.DOTALL)
    
    if match:
        transcript = match.group(1).strip()  # .group(1) = text after "Meeting Transcript:"
        transcript_format = rematch.group(1).strip() # group(1) text before "Meeting Transcript:"
    else:
        print("No Meeting Transcript found.")
    
    # Move model to GPU with float16 precision for better speed
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load the NLLB model and tokenizer
    model_name = script_dir / "models"/ "nllb-200-distilled-local"
    tokenizer = NllbTokenizer.from_pretrained(model_name)  # Use NllbTokenizer instead of AutoTokenizer

    # **Set Source Language (Tagalog)**
    tokenizer.src_lang = "tgl_Latn"

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.float16).to(device)

    # **Function to Extract Timestamps, Speaker Labels, and Text**
    def extract_parts(line):
        match = re.match(r"(\[\d+\.\d+ - \d+\.\d+\]) (SPEAKER \d+|UNKNOWN): (.*)", line)
        if match:
            timestamp, speaker, text = match.groups()
            return timestamp, speaker, text
        return None, None, line  # If no match, return the line unchanged

    # **Sentence Splitting Function (Chunking by Sentence)**
    def split_into_sentences(text):
        sentences = re.split(r'(?<=[.!?])\s+', text)  # Split using sentence boundaries
        return sentences

    # **Translate Sentences in Batches**
    def batch_translate(text_chunks):
        inputs = tokenizer(text_chunks, return_tensors="pt", padding=True, truncation=True).to(device)
        with autocast(device):
            translated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_length=150,
                repetition_penalty=1.5,
                no_repeat_ngram_size=3,
            )
        return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)

    # **Set target language (English)**
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("eng_Latn")

    # **Modify the Translation Loop**
    translated_lines = []
    for line in transcript.strip().split("\n"):
        timestamp, speaker, text = extract_parts(line)
        
        if text.strip():  # Only translate if there's dialogue
            text_chunks = split_into_sentences(text)
            # Translate sentences in batches
            translated_text = " ".join(batch_translate(text_chunks))
        else:
            translated_text = text  # Keep non-dialogue lines unchanged

        if timestamp and speaker:
            translated_lines.append(f"{timestamp} {speaker}: {translated_text}")
        else:
            translated_lines.append(translated_text)

    # **End Timer**
    end_time = time.time()

    # **Combine Translated Lines**
    final_translation = "\n".join(translated_lines)
    print(transcript_format + "\n\n" + final_translation)
    

    # Save the output_text to a text file   
    folder_outputs = "translations"
    makedirs(folder_outputs, exist_ok=True)
    output_file_path = join(folder_outputs, "translated_"+ file_name + ".txt")
    

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(transcript_format + "\n\n" + final_translation)
        
    _exit(0)

try:
    if __name__ == "__main__":
        if len(sys.argv) < 3:
            print("Error: Missing arguments. Usage: python translation.py <transcription, file_name>")
            sys.exit(1)  # Exit with an error

        meeting_id = sys.argv[1] 
        file_name = sys.argv[2]

        main(meeting_id, file_name)  # Call main() with extracted arguments

except Exception as e:
        print(f"Error has occured translation: {e}")

# finally:
#     print("Whole Process Completed")