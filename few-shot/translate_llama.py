import csv
from ContraDecode.translation_models.llama import LLaMaTranslationModel
import argparse
from langdetect import detect
import pandas as pd
from lang_dict import lang_dict
import os
import json

parser = argparse.ArgumentParser(description='Translate a file from a given source language to a target language with an OpenAI model.')
parser.add_argument('-l', '--level', required=True, type=str,choices=['para', 'sent'], help='Specify the translation level: paragraph-level or sentence-level')
parser.add_argument('--test', action='store_true', help='Specify whether it is a test (default: False)')
parser.add_argument('-r', '--run', required=False, type=str, help='Specify the run')

args = parser.parse_args()
level = args.level
run = args.run

input_dir = f"test_inputs" if args.test else f"../inputs/source_{level}_json"
output_dir = f"test_outputs" if args.test else f"translated/{level}-level"
os.makedirs(output_dir, exist_ok=True)

level_dict = {"para": "paragraph", "sent": "sentence"}
llama = LLaMaTranslationModel(model_name_or_path="meta-llama/Llama-2-70b-chat-hf", system_prompt="")
prompts_file = f"base_data/prompt_demonstrations_{level}.tsv"

# for promptline_type in ['InstructPromptline', 'KarpinskaPromptline','KarpinskaOneshot', 'InstructOneshot', 'MachineOneshot', 'HumanOneshot', 'HTMLOneshot']:

for promptline_type in ['HTMLOneshot']:
    
    with open("promptlines.json", "r") as f:
        promptlines = json.load(f) 
        prompttype = promptlines[promptline_type]["name"]

    for filename in os.listdir(input_dir):
        if "news" in filename:
            continue
        input_json = os.path.join(input_dir, filename)
        
        outputfilename = os.path.basename(filename)
        outputfilename = ".".join(outputfilename.split(".")[:-2]) + f".llama2.{prompttype}.{run}.csv"
        output_csv = os.path.join(output_dir, outputfilename)

        count = 0
        
        print("fixed input file: ", input_json)

        if "news" in filename:
            langs = filename.split("_")[0]
        else:
            langs = filename.split(".")[0]

        langs = langs.split("-")

        src_lang = langs[0]
        tgt_lang = langs[1]

        source_lang = lang_dict[src_lang]
        target_lang = lang_dict[tgt_lang]

        print("Source language = ", src_lang)
        print("Target language = ", tgt_lang)

        try:
            shots = pd.read_csv(prompts_file, sep="\t", encoding="utf-8")
            # select rows where column "code" is equal to source_lang-target_lang
            shots = shots.loc[shots['code'] == f"{src_lang}-{tgt_lang}"]
            # zip the columns "source" and "target" into a list of tuples
            zipped_shots = list(zip(shots["source"], shots["target"]))

            with open(input_json, "r") as inf, open(output_csv, "w", encoding="utf-8") as outf:

                writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["id", "source", "translation"])

                for line in inf:

                    source_text = json.loads(line)["source"]
                    if source_text == "":
                        continue
                    count += 1

                    promptline = promptlines[promptline_type]["promptline"].format(source_lang=source_lang, target_lang=target_lang, zipped_shots=zipped_shots, level=level_dict[level], source_text=source_text)
                    
                    print("*"*50)

                    new_prompt = f"You are a machine translation system that translates {level_dict[level]}s from {source_lang} to {target_lang}. You provide only the translation itself, with no additional comments."

                    llama.update_system_prompt(new_prompt)
                    
                    translations = llama.translate(
                        src_lang=source_lang,
                        tgt_lang=target_lang,
                        source_sentences=promptline,
                        num_beams=1,
                    )
                    print(llama.system_prompt)

                    print("TRANSLATION:")
                    print(translations)
                    print()

                    if len(translations) > 1:
                        if any([detect(translation) == tgt_lang for translation in translations[1:] if translation != ""]):
                            transls = []
                            for translation in translations[1:]:
                                if translation != "" and detect(translation) == tgt_lang and translation not in transls:
                                    transls.append(translation)
                            transls = " ** ".join(transls)
                            writer.writerow([count, source_text, transls.replace("\n", " ")])
                        else:
                            writer.writerow([count, source_text, f"NO {target_lang} DETECTED"])

                    elif len(translations) == 1 and detect(translations[0]) == tgt_lang:
                        writer.writerow([count, source_text, translations[0].replace("\n", " ")])
                    elif len(translations) == 1 and detect(translations[0]) != tgt_lang:
                        writer.writerow([count, source_text, f"NO {target_lang} DETECTED"])
        
        except IndexError:
            print(f"PROBLEM with {outputfilename}")
            continue