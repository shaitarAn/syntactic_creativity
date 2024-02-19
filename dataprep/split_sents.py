import os
from wtpsplit import WtP
import sys
import csv
import json
import string
import argparse
from utils import *

os.environ['CUDA_VISIBLE_DEVICES'] = '2'  # for one GPU

wtp = WtP("wtp-bert-mini")
wtp.half().to("cuda:0")


inputdir = "source_para_json"
outputdir = "source_sent_json"
outputdir2 = "source_sent_txt"

# make sure the output directory exists
if not os.path.exists(outputdir):
    os.makedirs(outputdir)
if not os.path.exists(outputdir2):
    os.makedirs(outputdir2)


def is_only_punctuation(text):
    additional_punctuation = "」。"  # Add the characters you want to include here
    if all(char in string.punctuation or char in additional_punctuation for char in text.strip()):
        return True
    
def has_digit(text):
    if text.strip().replace(".", "").isdigit() or text.strip().replace(")", "").isdigit():
        return True

# Define a variable to store the buffer
punctuation_buffer = ""

# iterate through the data directory
for file in os.listdir(inputdir):
    if file.endswith("json"):
        file = os.path.join(inputdir, file)
        filename = os.path.basename(file)
        print(filename)

        if "news" in filename:
            langs = filename.split("_")[0]
        else:
            langs = filename.split(".")[0]
        
        lang = langs.split("-")[0]
        print(lang)

        outputfilename = os.path.join(outputdir, filename)
        outputfilename = outputfilename.replace("para", "sent")
        textfile = os.path.join(outputdir2, filename)
        txtf = textfile.replace("json", "txt")


        with open(file, "r") as inf, open(outputfilename, "w") as outf, open(txtf, "w") as outft:
            for line in inf:
                source_text = json.loads(line)["source"]
                if lang == "ja":
                    source_text = normalize_japanese_punct(source_text)
                elif lang == "de":
                    source_text = normalize_german_punct(source_text)

                else:               
                    source_text = normalize_punct(source_text)
                source_text = capitalize_after_period_space(source_text)
                source_text = wtp.split(source_text, lang_code=lang, style="ud")

                for sent in source_text:
                    sent = sent.replace("\n", " ")
                    sent = sent.lstrip()
                    # print(sent)
                    if has_digit(sent):
                        # Append the punctuation-only line to the buffer
                        punctuation_buffer += sent.strip() + " "
                    elif is_only_punctuation(sent):
                        continue
                    else:
                        # If the current line is not punctuation-only, write the buffer and reset it
                        if punctuation_buffer:
                            sent = punctuation_buffer + sent
                            punctuation_buffer = ""
                        
                        # Write the sentence to the output files
                        json.dump({"source": sent.strip()}, outf)
                        outf.write("\n")
                        outft.write(sent.strip() + "\n")

            # Write any remaining content in the buffer to the output files
            if punctuation_buffer:
                json.dump({"source": punctuation_buffer.strip()}, outf)
                outf.write("\n")
                outft.write(punctuation_buffer.strip() + "\n")

# print(string.punctuation)

