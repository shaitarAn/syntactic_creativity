import os
import openai
import requests
import json
import re
import sys
import csv
import argparse
from lang_dict import lang_dict
from config import *

openai.organization = ORGANIZATION
openai.api_key = OPENAI_API_KEY

parser = argparse.ArgumentParser(description='Translate a file from a given source language to a target language with an OpenAI model.')
parser.add_argument('-f', '--infile', required=True, help='the file to be translated')
parser.add_argument('-sl', '--source_lang', required=False, help='source language (default: en).', default='en')
parser.add_argument('-tl', '--target_lang', required=False, help='target language (default: de).', default='de')
parser.add_argument('-o', '--output_dir', required=True, help='the output directory of the translated file.')
parser.add_argument('-m', '--mtsystem', required=False, help='the machine translation system to be used (default: gpt-3.5-turbo-16k).', default='gpt-3.5-turbo-16k')
parser.add_argument('-tmp', '--temperature', required=False, help='temperature (default: 0.7).', default=0.7)
parser.add_argument('-fp', '--frequency_penalty', required=False, help='frequency penalty (default: 0.5).', default=0.5)
parser.add_argument('-l', '--level', required=True, help='paragraph-level or sentence-level translation')
parser.add_argument('-t', '--task', required=False, help='write or append to file (default: write).', default='w')
parser.add_argument('-c', '--count', required=True, help='start counting lines from this number (default: 0).', default=0)

args = parser.parse_args()

infile = args.infile
output_dir = args.output_dir

source_lang = lang_dict[args.source_lang]
target_lang = lang_dict[args.target_lang]

temperature = int(args.temperature)
frequency_penalty = int(args.frequency_penalty)

level = args.level
task = args.task
startCount = int(args.count)

if "gpt-3.5" in args.mtsystem:
    mts = "gpt3"
elif "gpt-4" in args.mtsystem:
    mts = "gpt4"

langs_data = os.path.basename(infile).split(".")[0]

output = os.path.join(output_dir, f"{langs_data}.{level}.{mts}.csv")

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai.api_key}'
    }


try:
    # open json file
    with open(infile, "r") as inf, open(output, task) as outf:

        writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "source", "translation"])
        count = startCount

        for line in inf:
            source_text = json.loads(line)["source"]
            if source_text == "":
                continue
            count += 1

            promptline = f"Translate the following text into {target_lang}. Output only the translation itself without additional commentary or explanations. Text: " + source_text
            prompt =[{
                "role": "system",
                "content": f"You are a translator from {source_lang} to {target_lang}."
                },{
                "role": "user",
                "content": promptline
                }]
            data = {
                'model': args.mtsystem,
                'messages':prompt,
                "max_tokens":1500,
                "temperature":temperature,
                "frequency_penalty":frequency_penalty,
                "presence_penalty":0,
                "seed":23,
            }

            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,data=json.dumps(data))

            print(count)

            # Check response status
            if response.status_code == 200:
                result = response.json()

                raw_output = result["choices"][0]["message"]["content"]
                # print(raw_output)
                writer.writerow([count, source_text, raw_output.strip().replace("\n", " ")])
            else:
                print(count, source_text, "<ERROR>")
                print("Re-translating...")
                
                # Revert file pointer to the previous position to resend the same text for translation
                response_new = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,data=json.dumps(data))

                if response_new.status_code == 200:
                    result_new = response_new.json()
                    raw_output_new = result_new["choices"][0]["message"]["content"]
                    print(raw_output_new)
                    writer.writerow([count, source_text, raw_output_new.strip().replace("\n", " ")])
                else:
                    print(count, source_text, "<ERROR>")
                    writer.writerow([count, source_text, "<ERROR>"])
                    

except Exception as e:
    print(e)
    print("ERROR: something went wrong with the translation. The file {} might be empty.".format(infile), file=sys.stderr)
    pass
