from transformers import AutoTokenizer
import csv
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-chat-hf")
tokenizer.encode("Hello this is a test")

source_lang = "Cheque"
target_lang = "Polish"

prompt_file = "base_data/prompt_demonstrations_para.tsv"
prompts = pd.read_csv(prompt_file, sep="\t", encoding="utf-8")
# select rows where column "code" is equal to source_lang-target_lang
prompts = prompts.loc[prompts['code'] == "cs-pl"]

# zip the columns "source" and "target" into a list of tuples
zipped_shots = list(zip(prompts["source"], prompts["target"]))

source_text = "Sedl si ke stolku vedle mě a otevřel desky, který jsem mu dala, a začal si prohlížet obrázky jeden po druhým. Na některý se díval docela dlouho, úplně je zkoumal, takže mi bylo jasný, že musí vidět všechny chyby, co na nich jsou. A taky že poznal, kdy už se mi na tom obrázku nechtělo dělat a jen jsem to tak doplácala barvama. Potom vzal ten výkres s vránama a řekl, že ten se mu líbí nejvíc. A usmíval se a vypadal ještě víc jako Frodo. Všimla jsem si, že má takový krásně dlouhý prsty s kulatejma nehtama."

promptline = f"Original text in {source_lang}: {zipped_shots[0][0]} Translation into {target_lang}: {zipped_shots[0][1]} Original text in {source_lang}: {zipped_shots[1][0]} Translation into {target_lang}: {zipped_shots[1][1]} Original text in {source_lang}: {zipped_shots[2][0]} Translation into {target_lang}: {zipped_shots[2][1]} Original text in {source_lang}: {zipped_shots[3][0]} Translation into {target_lang}: {zipped_shots[3][1]} Original text in {source_lang}: {zipped_shots[4][0]} Translation into {target_lang}: {zipped_shots[4][1]} Original text in {source_lang}: {source_text} Translation into {target_lang}:"

print(len(tokenizer.encode(promptline)))