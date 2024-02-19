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
    return all(char in string.punctuation or char in additional_punctuation for char in text.strip())

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
                    source_text = replace_full_stop_char(source_text)
                
                source_text = normalize_punct(source_text)
                source_text = capitalize_after_period_space(source_text)
                source_text = wtp.split(source_text, lang_code=lang, style="ud")

                for sent in source_text:
                    sent = sent.replace("\n", " ")
                    sent = sent.lstrip()
                    # print(sent)
                    if not is_only_punctuation(sent):
                        json.dump({"source": sent.strip()}, outf)
                        outf.write("\n")
                        outft.write(sent.strip() + "\n")

# print(string.punctuation)

