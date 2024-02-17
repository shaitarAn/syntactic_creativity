import os
import openai
import requests
import json
import re
import sys
import csv
from lang_dict import lang_dict

level = "sent"


openai.organization = "org-HjWBseLU0iDzg4cx01nO6JrY"
openai.api_key = "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"

languages = re.compile(r"(\w\w-\w\w)_.*")
output_dir = f"data/llama_translations/llama_{level}_gpt4_cleaned_news"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

meta_data_dir = f"data/extras/llama_{level}_txt_clean_meta"
if not os.path.exists(meta_data_dir):
    os.makedirs(meta_data_dir)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai.api_key}'
    }

# create a meta data dictionary
meta_data = {}

# iterate over csv files in input directory
for file in os.listdir(f"data/llama_translations/llama_{level}_csv_news"):
    file = os.path.join(f"data/llama_translations/llama_{level}_csv_news", file)
    #  extract filename without extension
    filename = os.path.basename(file)
    # # extract language codes from filename
    match = languages.search(file)
    if match:
        langs = match.group(1)
        source_lang = langs.split("-")[0]
        target_lang = langs.split("-")[1]
        source_lang = lang_dict[source_lang]
        target_lang = lang_dict[target_lang]
        # open and read csv file
        # create new csv file in output directory
        # create a json file in meta data directory       
        with open(file, 'r') as inf, open(output_dir + "/" + filename, 'w') as outf, open(meta_data_dir + "/" + filename + ".jsonl", 'w') as meta_outf:
            reader = csv.reader(inf, delimiter=',', quotechar='"')
            # skip header
            next(reader)

            writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["id", "source", "translation"])

            for row in reader:
                line_num = row[0]
                source = row[1]
                translation = row[2]

                # if source txt contains no alphabetic characters in any language, skip
                if not re.search(r"[^\W\d_]", source, re.UNICODE):
                    continue

                elif source == "–":
                    continue

                else:
                
                    print(file)
                    print("***", source_lang, source)
                    print("***", target_lang, translation)
                    print()
                    # print("---------------------------------")
            
                    # promptline = f"Here is the source text in {source_lang}: {row[1]}. Here is the target text which is a translation into {target_lang} by a large language model: {row[2]}. The translation model left many commentaries and notes. Moreover, the translation is sometimes in a wrong target language. Identify if a proper translation from {source_lang} to {target_lang} is present. If a translation is found, output only the translation itself. If no translation is found, return the following text: 'NO TRANSLATION FOUND' plus the target text."

                    promptline = f"Here is the source text in {source_lang}: {source}. Here is the target text: {translation}. Identify if the target text includes a {target_lang} translation of the source text. If it does, return the {target_lang} translation. If the target text contains no translation of the source text, return 'NO TRANSLATION FOUND' plus the target text. If the translation is in the wrong language, return 'NO TRANSLATION FOUND' plus the target text. If {target_lang} translation is in {translation} return only the translation itself."

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
                            new_promptline = f"Here is the source text: {row[1]}. Verify that there is trully no {target_lang} translation of the source text in this output: {raw_output}. If you find the {target_lang} translation, return <<WRONG STATEMENT, TRANSLATION FOUND>> plus the translation itself. If you find the inaccurate {target_lang} translation, please return <<INACCURATE TRANSLATION>> plus the translation itself. If there is indeed no translation found, return <<CORRECT STATEMENT, NO TRANSLATION FOUND, because>> plus explanation and the original target text."
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
                            writer.writerow([line_num, source.replace("\n", ""), new_raw_output.strip().replace("\n", "")])
                            # write to meta json file
                            meta_outf.write(json.dumps(new_result))

                        else:
                            print(raw_output)
                            print("------------------------------------------------------------------")
                            print()
                            writer.writerow([line_num, source.replace("\n", ""), raw_output.strip().replace("\n", "")])
                            meta_outf.write(json.dumps(result))
                    else:
                        print(response.json())
                        writer.writerow([line_num, source, "<ERROR>"])

