from prompts import translation_into, lang_instructions
from lang_dict import lang_dict
import pandas as pd

print(lang_dict)

for key, value in lang_dict.items():
    print(f"{key}: {value}")

level = "para"
src_lang = "cs"
tgt_lang = "pl"

source_lang = lang_dict[src_lang]
target_lang = lang_dict[tgt_lang]

prompts_file = f"base_data/prompt_demonstrations_{level}.tsv"

prompts = pd.read_csv(prompts_file, sep="\t", encoding="utf-8")
# select rows where column "code" is equal to source_lang-target_lang
prompts = prompts.loc[prompts['code'] == f"{src_lang}-{tgt_lang}"]
# zip the columns "source" and "target" into a list of tuples
zipped_prompts = list(zip(prompts["source"], prompts["target"]))

promptline = f"""Learn to translate {source_lang} into {target_lang}
            from these examples: \n
            **** Original text in {source_lang}: {zipped_prompts[0][0]}\n
            888 {translation_into[tgt_lang]}: {zipped_prompts[0][1]}\n
            **** Original text in {source_lang}: {zipped_prompts[1][0]}\n
            888 {translation_into[tgt_lang]}: {zipped_prompts[1][1]}\n            
            **** Original text in {source_lang}: {zipped_prompts[2][0]}\n
            888 {translation_into[tgt_lang]}: {zipped_prompts[2][1]}\n           
            **** Original text in {source_lang}: {zipped_prompts[3][0]}\n
            888 {translation_into[tgt_lang]}: {zipped_prompts[3][1]}\n            
            **** Original text in {source_lang}: {zipped_prompts[4][0]}\n
            888 {translation_into[tgt_lang]}: {zipped_prompts[4][1]}\n
            7777777 {lang_instructions[tgt_lang].format(source_text="source_text")}
            """


print(promptline.replace("\n", "******************************\n"))

