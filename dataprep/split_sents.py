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
outputdir = "source_sent_json"
outputdir2 = "source_sent_txt"

# make sure the output directory exists
if not os.path.exists(outputdir):
    os.makedirs(outputdir)
if not os.path.exists(outputdir2):
    os.makedirs(outputdir2)

# Define a variable to store the buffer
punctuation_buffer = ""

def preprocess_text(source_text, lang):
    if lang == "ja":
        source_text = normalize_japanese_punct(source_text)
    elif lang == "de":
        source_text = normalize_german_punct(source_text)

    else:               
        source_text = normalize_punct(source_text)
    source_text = capitalize_after_period_space(source_text)

    return source_text

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
            for row in reader:
                source_text = row[1]
                source_text = preprocess_text(source_text, lang)   

                # split texts into sentences
                source_sents = wtp.split(source_text, lang_code=lang, style="ud")

                for sent in source_sents:
                    sent = sent.replace("\n", " ")
                    sent = sent.lstrip()

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


