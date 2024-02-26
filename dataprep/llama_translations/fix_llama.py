import csv
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from translation_models.llama import LLaMaTranslationModel
import argparse
import os

llama = LLaMaTranslationModel(model_name_or_path="meta-llama/Llama-2-70b-chat-hf")
error_strings=["CORRECT STATEMENT, NO TRANSLATION FOUND", "<ERROR>"] # Define the error string to search for

input_dir = "/data/ashait/inputs/llama_sent_gpt4_cleaned/"
output_dir = "/data/ashait/outputs/fixed_sent"
os.makedirs(output_dir, exist_ok=True)

for input_csv in os.listdir(input_dir):

    filename = os.path.basename(input_csv)
    input_csv = os.path.join(input_dir, filename)
    output_csv = os.path.join(output_dir, filename)
    print("fixed input file: ", input_csv)

    if "news" in filename:
        langs = filename.split("_")[0]
    else:
        langs = filename.split(".")[0]

    langs = langs.split("-")
    src_lang = langs[0]
    tgt_lang = langs[1]
    print("Source language = ", src_lang)
    print("Target language = ", tgt_lang)

    with open(input_csv, "r", encoding="utf-8") as inf, open(output_csv, "w", encoding="utf-8") as outf:
        reader = csv.reader(inf, delimiter=',')
        # skip header
        next(reader)

        writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "source", "translation"])

        for row in reader:
            # if any of the errors from the error_strings is in row[2]
            if any(error in row[2] for error in error_strings):

                translations = llama.translate(
                    src_lang=src_lang,
                    tgt_lang=tgt_lang,
                    source_sentences=[row[1]],
                    num_beams=1,
                )

                print(translations)
                writer.writerow([row[0], row[1], translations[0].replace("\n", " ")])
            
            else:
                writer.writerow(row)