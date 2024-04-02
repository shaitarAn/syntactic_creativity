import os
import openai
import requests
import json
import re
import sys
import csv
from lang_dict import lang_dict
from keys import * 

level = "sent"
startline = 1

openai.organization = ORGANIZATION
openai.api_key = OPENAI_API_KEY

output_dir = f"llama_translations/llama_{level}_gpt4_cleaned"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

meta_data_dir = f"llama_translations/llama_{level}_txt_clean_meta"
if not os.path.exists(meta_data_dir):
    os.makedirs(meta_data_dir)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai.api_key}'
    }

# create a meta data dictionary
meta_data = {}

# iterate over csv files in input directory
for file in os.listdir(f"llama_translations/llama_{level}_csv"):
    file = os.path.join(f"llama_translations/llama_{level}_csv", file)
    #  extract filename without extension
    filename = os.path.basename(file)
    langs = ""

    if "news" in filename:
        langs = filename.split("_")[0]
    else:
        langs = filename.split(".")[0]
    
    source_lang = langs.split("-")[0]
    target_lang = langs.split("-")[1]        
    source_lang = lang_dict[source_lang]
    target_lang = lang_dict[target_lang]

    # Determine the mode based on the line number
    mode = 'w' if startline == 1 else 'a'

    with open(file, 'r') as inf, open(output_dir + "/" + filename, mode) as outf, open(meta_data_dir + "/" + filename + ".jsonl", mode) as meta_outf:
        reader = csv.reader(inf, delimiter=',', quotechar='"')
        # skip header
        next(reader)

        writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write header only if starting from line 1
        if mode == 'w':
            writer.writerow(["id", "source", "translation"])

        for row in reader:
            if int(row[0]) < startline:
                continue
            line_num = row[0]
            source = row[1]
            translation = row[2]
            
            print(file)
            print("***", source_lang, source)
            print("***", target_lang, translation)
            print()
            # print("---------------------------------")

            promptline = f"Here is the source text in {source_lang}: {source}. Here is the target text: {translation}. Does the target text include a {target_lang} translation of the source text? If TRUE, copy that {target_lang} translation and return it, omitting all other text. If FALSE, return 'NO TRANSLATION FOUND' plus the target text. If the translation is not in {target_lang}, also return 'NO TRANSLATION FOUND' plus the target text."

            prompt =[{
                "role": "system",
                "content": f"You are a machine that can identify translations from {source_lang} to {target_lang}. You execute commands without adding any additional comments or explanations."
                },{
                "role": "user",
                "content": promptline
                }]
            data = {
                'model': "gpt-4",
                'messages':prompt,
                "max_tokens":1500,
                "temperature":1,
                "frequency_penalty":1,
                "presence_penalty":0,
                "logprobs": True,
                "top_logprobs": 3,
                "seed": 23,
            }

            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,data=json.dumps(data))

            print(response.status_code)

            # check 
            if response.status_code == 200:
                result = response.json()
                # write output to file in the meta data directory
                json.dump(result, meta_outf)

                raw_output = result["choices"][0]["message"]["content"]
                if "NO TRANSLATION FOUND" in raw_output:
                    new_promptline = f"Here is the source text: {row[1]}. Verify that there is trully no {target_lang} translation of the source text in this text: {raw_output}. If you find the {target_lang} translation, return <<WRONG STATEMENT, TRANSLATION FOUND>> plus the translation itself. If you determine that the {target_lang} translation is inaccurate, please return <<INACCURATE TRANSLATION>> plus the translation itself. If there is indeed no translation found, return <<CORRECT STATEMENT, NO TRANSLATION FOUND, because>> plus explanation and the original target text."
                    new_prompt =[{
                        "role": "system",
                        "content": f"You are a controller that verifies the work of a translation editor. Translation editor made a claim that NO TRANSLATION FOUND. Your job is to verify that statement. You execute commands without adding any additional comments or explanations."
                        },{
                        "role": "user",
                        "content": new_promptline
                        }]
                    new_data = {
                        'model': "gpt-4",
                        'messages':new_prompt,
                        "max_tokens":1500,
                        "temperature":1,
                        "frequency_penalty":1,
                        "presence_penalty":0,
                        "logprobs": True,
                        "top_logprobs": 3,
                        "seed": 23,
                    }
                    new_response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,data=json.dumps(new_data))
                    new_result = new_response.json()
                    new_raw_output = new_result["choices"][0]["message"]["content"]
                    print("new_raw_output: ", new_raw_output)
                    print("------------------------------------------------------------------")
                    print()
                    writer.writerow([line_num, source, new_raw_output.strip()])
                    # write to meta json file
                    meta_outf.write(json.dumps(new_result))

                else:
                    print(raw_output)
                    print("------------------------------------------------------------------")
                    print()
                    writer.writerow([line_num, source, raw_output.strip()])
                    meta_outf.write(json.dumps(result))
            else:
                print(response.json())
                writer.writerow([line_num, source, "<ERROR>"])

    startline = 1

# f'<s> [INST] <<SYS>> 
# You are a proffessional translator from {{ source_lang }} into {{ target_lang }}. 
# <</SYS>> Translate the following text from {{ source_lang }} into {{ target_lang }}. 
# Output only the translation itself without additional commentary or explanations. 
# Text: {{ instruction }} [/INST]'


