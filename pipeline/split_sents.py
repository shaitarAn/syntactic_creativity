import os
from wtpsplit import WtP
import sys
import csv
import string
import argparse
from utils import *

os.environ['CUDA_VISIBLE_DEVICES'] = '2'  # for one GPU

wtp = WtP("wtp-bert-mini")
wtp.half().to("cuda:0")

parser = argparse.ArgumentParser()
parser.add_argument("--indir", "-i", type=str)
parser.add_argument("--outdir", "-o", type=str)
args = parser.parse_args()

inputdir = args.indir
outputdir = args.outdir

# make sure the output directory exists
if not os.path.exists(outputdir):
    os.makedirs(outputdir)

def is_only_punctuation(text):
    additional_punctuation = "」。"  # Add the characters you want to include here
    return all(char in string.punctuation or char in additional_punctuation for char in text.strip())

# iterate through the data directory
for file in os.listdir(inputdir):
    if file.endswith("txt"):
        file = os.path.join(inputdir, file)
        filename = os.path.basename(file)
        print(filename)
        if "news" in filename:
            langs = filename.split("_")[0]
        else:
            langs = filename.split(".")[0]
        if "source" in file:
            lang = langs.split("-")[0]
        else:
            lang = langs.split("-")[1]
        print(lang)

        outputfilename = os.path.join(outputdir, filename)
        if "asis" in outputfilename:
            outputfilename = outputfilename.replace("asis", "split")
            print(outputfilename)
        else:
            outputfilename = outputfilename.replace(".txt", ".split.txt")
        print(outputfilename)
        print("----------------------------------")

        with open(file, "r") as inf, open(outputfilename, "w") as outf:
            text = inf.read().replace("\n", " ")
            if lang == "ja":
                text = replace_full_stop_char(text)
            
            text = normalize_punct(text)
            text = capitalize_after_period_space(text)
            text = wtp.split(text, lang_code=lang, style="ud")

            for sent in text:
                sent = sent.replace("\n", " ")
                sent = sent.lstrip()
                # print(sent)
                if not is_only_punctuation(sent):
                    outf.write(sent.strip() + "\n")

# print(string.punctuation)

