import time
# **Start Timer**
start_time = time.time()
import torch
import re
from transformers import NllbTokenizer,AutoModelForSeq2SeqLM  # Change AutoTokenizer to NllbTokenizer
from torch.amp import autocast  # Import from torch.amp instead of torch.cuda.amp
from pathlib import Path
from os import makedirs
from os.path import join, basename
import sys

def main(file_path):
    print("translation started")
    script_dir = Path(__file__).parent
    print(file_path)

    # Move model to GPU with float16 precision for better speed
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(device)

    # Load the NLLB model and tokenizer
    model_name = script_dir.parent / "models"/ "models--facebook--nllb-200-distilled-1.3B" /"snapshots"/"f9e6ff7fc090740fcce5af7d7636cb27a33d0f18"
    tokenizer = NllbTokenizer.from_pretrained(model_name)  # Use NllbTokenizer instead of AutoTokenizer

    # **Set Source Language (Tagalog)**
    tokenizer.src_lang = "tgl_Latn"

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.float16).to(device)

    with open(file_path, 'r', encoding='utf-8') as file:
        tagalog_text = file.read()  # Read the entire file content

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
    for line in tagalog_text.strip().split("\n"):
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
    print("Translated Text:\n", final_translation)

    file_name = basename(file_path)
    print("File Name:", file_name)
    file_name = file_name.replace("fixed_", "")  # Remove "fixed_" from the file name
    file_name = file_name.replace(".mp3.txt", ".txt")  # Remove ".mp3.txt" from the file name

    print("File Name:", file_name)
    # Save the output_text to a text file   
    folder_outputs = "translations"
    makedirs(folder_outputs, exist_ok=True)
    output_file_path = join(folder_outputs, "translated_"+ file_name)

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(final_translation)

    # **Print time taken**
    print(f"Translation Time: {end_time - start_time:.2f} seconds")

try:
    if __name__ == "__main__":
        if len(sys.argv) < 2:
            print("Error: Missing arguments. Usage: python translation.py <file_path>")
            sys.exit(1)  # Exit with an error

        file_path = sys.argv[1]  # Get first argument (audio file path)

        main(file_path)  # Call main() with extracted arguments
    # if __name__ == "__main__":
    #     output=main("C:/Users/joech/Desktop/Transcription/Audios/ariana filler.mp3", 2)
    #     #C:/Users/joech/Desktop/4thYear1stSem/Audios Unused
except Exception as e:
        print(f"Error has occured: {e}")

finally:
    print("Whole Process Completed")