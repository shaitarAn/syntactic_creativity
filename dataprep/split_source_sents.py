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


inputdir = "all_csv"
outputdir = "../inputs/source_sent_json"
outputdir2 = "source_sent_txt"

# make sure the output directory exists
if not os.path.exists(outputdir):
    os.makedirs(outputdir)
if not os.path.exists(outputdir2):
    os.makedirs(outputdir2)

# Define a variable to store the buffer
punctuation_buffer = ""

# iterate through the data directory
for file in os.listdir(inputdir):
    if file.endswith("human.csv"):
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
        outputfilename = outputfilename.replace("para", "sent").replace("csv", "json").replace("human", "source")
        textfile = os.path.join(outputdir2, filename)
        txtf = textfile.replace("csv", "txt").replace("human", "source")


        with open(file, "r") as inf, open(outputfilename, "w") as outf, open(txtf, "w") as outft:
            reader = csv.reader(inf)
            next(reader)

            sentences = split_sentences(reader, lang, wtp, col=1)

            for s in sentences:
                json.dump({"source": s.strip()}, outf)
                outf.write("\n")
                outft.write(s.strip() + "\n")


