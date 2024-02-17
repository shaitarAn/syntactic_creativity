import argparse
import requests
import sys
import json
import os

input = "data/final/paras_split_into_sents/source/de-en_news.para.source.split.txt"
output = "output/de-en_news.sents.deepl.asis.txt"

bad = ['Ã¤', 'Ã¼', 'Ã¶', 'Ã„', 'Ã£', 'Ã¨', 'Ãª', 'Ã\x9f', 'Ã˜']
odd = '체'

try:
    with open(input, 'r') as inf, open(output, 'w', encoding="utf8") as outf:
        for line in inf:
            line = line.strip()
            print(line)
            if line:

                data = {
                    'auth_key': '9a6fc970-247c-ea3a-60d0-029b20d818ad:fx',
                    'text': line,
                    'target_lang': 'EN'
                }

                response = requests.post('https://api-free.deepl.com/v2/translate', data=data)
                # response = requests.post('https://api.deepl.com/v2/translate', data=data)
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

# Daniel's: 9a6fc970-247c-ea3a-60d0-029b20d818ad:fx
# Institute's: 233c7e16-b716-f5b0-95e0-7aadaa86a47e
# Mine: 26a5dce0-e069-d906-abc4-9c9f9e5af3e7:fx
# Lukas: b72e2fd3-baca-95b3-6c80-cc37b53087ef

# one line test
# import requests
# line = 'You can come back any time as our chat service window is open 24/7'
# data = {'auth_key': '26a5dce0-e069-d906-abc4-9c9f9e5af3e7:fx','text': line,'target_lang': 'DE'}
# response = requests.post('https://api-free.deepl.com/v2/translate', data=data)
# print(response.text)
# # => {"translations":[{"detected_source_language":"EN","text":"Sie können jederzeit wiederkommen, da unser Chatfenster 24/7 geöffnet ist."}]}

