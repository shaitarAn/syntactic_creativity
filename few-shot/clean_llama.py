import csv
import os
import argparse
from ContraDecode.translation_models.llama import LLaMaTranslationModel
from lang_dict import lang_dict

parser = argparse.ArgumentParser(description='Clean llama2-translated texts using llama2 chain-of-thought prompting and html tags.')
parser.add_argument('-l', '--level', required=True, help='paragraph-level or sentence-level translation')

args = parser.parse_args()
level = args.level

llama = LLaMaTranslationModel(model_name_or_path="meta-llama/Llama-2-70b-chat-hf", system_prompt="")

input_dir = f"translated_temp0.1/{level}-level"
output_dir = f"translated_html/{level}-level"
os.makedirs(output_dir, exist_ok=True)


for filename in os.listdir(input_dir):
    filename = os.path.basename(filename)
    inputfile = os.path.join(input_dir, filename)
    outputfile = os.path.join(output_dir, filename)
    langs = filename.split(".")[0]

    langs = langs.split("-")
    src_lang = langs[0]
    tgt_lang = langs[1]
    source_lang = lang_dict[src_lang]
    target_lang = lang_dict[tgt_lang]

    print("Source language = ", src_lang)
    print("Target language = ", tgt_lang)

    with open(inputfile, "r") as inf, open(outputfile, "w", encoding="utf-8") as outf:

        reader = csv.reader(inf)
        next(reader)
        writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "source", "translation"])

        for line in reader:

            source_text = line[1]
            count = line[0]
            translation = line[2]

            if source_text == "":
                continue

            promptline = f"Here is the source text in {source_lang}: {source_text}. Here is the trandslation: {translation}. Analyze the translation and think step-by-step. Identify and extract the {target_lang} translation of the source text and return it between <p> and </p> as one HTML paragraph. If some translated sentence within the paragraph repeats itself, return only one copy of that sentence. If the {target_lang} translation is absent, return 'NO TRANSLATION FOUND' plus the target text."

            new_prompt=f"You are a machine that can identify translations from {source_lang} to {target_lang}. You execute commands without adding any additional comments or explanations. Your level of verbosity is zero.",

            llama.update_system_prompt(new_prompt)
            
            translations = llama.translate(
                src_lang=source_lang,
                tgt_lang=target_lang,
                source_sentences=promptline,
                num_beams=1,
                )

            if "NO TRANSLATION FOUND" in translations:
                new_promptline = f"Here is the source text: {source_text}. Verify that there is trully no {target_lang} translation of the source text in this text: {translations}. Let's think step-by-step. If you find the {target_lang} translation, extract the translation itself and return it between <p> and </p> as one HTML paragraph . If there is indeed no translation found, translate the source text into {target_lang} and return it as one HTML paragraph between <p> and </p>."

                controller_prompt="You are a controller that verifies the work of a translation editor. Translation editor made a claim that NO TRANSLATION FOUND. Your job is to verify that statement. You execute commands without adding any additional comments or explanations."

                llama.update_system_prompt(controller_prompt)

                translations = llama.translate(
                src_lang=source_lang,
                tgt_lang=target_lang,
                source_sentences=new_promptline,
                num_beams=1,
                )

                print("TRANSLATION 2nd round:")
                print(translations)
                print()

                writer.writerow([count, source_text, translations.replace("\n", " ")])
            else:
                print("TRANSLATION 1st round:")
                print(translations)
                print()
                writer.writerow([count, source_text, translations.replace("\n", " ")])