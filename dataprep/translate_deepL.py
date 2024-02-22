import argparse
import requests
import sys
import json
import os
from config import DEEPL_KEY

parser = argparse.ArgumentParser(description='Translate text using DeepL')
parser.add_argument('-f', '--inputfile', help='input file')
parser.add_argument('-o', '--output', help='output file')
parser.add_argument('-tl', '--targetlang', help='target language')

args = parser.parse_args()

input = args.inputfile
output = args.output
# capitalize target language
targetlang = args.targetlang.upper()

bad = ['Ã¤', 'Ã¼', 'Ã¶', 'Ã„', 'Ã£', 'Ã¨', 'Ãª', 'Ã\x9f', 'Ã˜']
odd = '체'

try:
    with open(input, 'r') as inf, open(output, 'w', encoding="utf8") as outf:
        for line in inf:
            line = line.strip()
            print(line)
            if line:

                data = {
                    'auth_key': DEEPL_KEY,
                    'text': line,
                    'target_lang': targetlang
                }

                # response = requests.post('https://api-free.deepl.com/v2/translate', data=data)
                response = requests.post('https://api.deepl.com/v2/translate', data=data)
                print(response)

                my_response = response.text

                if response.ok:
                    if odd in my_response:
                        my_response = my_response.encode('cp949').decode('utf-8')
                    else:
                        try:
                            my_response = my_response.encode('latin_1').decode('utf-8')
                        except UnicodeDecodeError:
                            my_response = response.text
                        except UnicodeEncodeError:
                            try:
                                my_response = response.text.encode('cp1252').decode('utf-8')
                            except:
                                my_response = response.text

                dict = json.loads(my_response)
                try:
                    raw_output = dict['translations'][0]['text']
                except KeyError:
                    raw_output = '###TO BE TRANSLATED###{}'.format(line)
                    print(raw_output, file=sys.stderr)

                outf.write(raw_output + "\n")
                print(raw_output)
                print()
            print("--------------")

except TypeError:
    raise

# sed -n '3491,7147p' ../../output/gutenberg_raw_en.txt > ../../output/gutenberg_raw_en_1.txt

# one line test
# import requests
# line = 'You can come back any time as our chat service window is open 24/7'
# data = {'auth_key': DEEPL_KEY,'text': line,'target_lang': 'DE'}
# response = requests.post('https://api-free.deepl.com/v2/translate', data=data)
# print(response.text)
# # => {"translations":[{"detected_source_language":"EN","text":"Sie können jederzeit wiederkommen, da unser Chatfenster 24/7 geöffnet ist."}]}

