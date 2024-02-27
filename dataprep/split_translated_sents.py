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

level = "sent"

inputdir = f"../inputs/{level}s"
outputdir = f"../inputs/target_sent_json_{level}-level"

# make sure the output directory exists
if not os.path.exists(outputdir):
    os.makedirs(outputdir)

# Define a variable to store the buffer
punctuation_buffer = ""

# iterate through the data directory
for file in os.listdir(inputdir):
    if file.endswith(".csv"):
        file = os.path.join(inputdir, file)
        filename = os.path.basename(file)
        print(filename)
        system = filename.split(".")[2]

        if "news" in filename:
            langs = filename.split("_")[0]
        else:
            langs = filename.split(".")[0]
        
        lang = langs.split("-")[1]
        print(lang)

        outputfilename = os.path.join(outputdir, filename)
        outputfilename = outputfilename.replace("csv", "split.json")


        with open(file, "r") as inf, open(outputfilename, "w") as outf:
            reader = csv.reader(inf)
            next(reader)

            sentences = split_sentences(reader, lang, wtp, col=2)

            for s in sentences:
                json.dump({"translation": s.strip()}, outf)
                outf.write("\n")


