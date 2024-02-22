import json
import os
import argparse
import csv
from utils import *

# convert csv to json for Llama where each line has the following format: {"source": "Lead researchers say this may bring early detection of cancer, tuberculosis, HIV and malaria to patients in low-income countries, where the survival rates for illnesses such as breast cancer can be half those of richer countries."}

parser = argparse.ArgumentParser()
parser.add_argument("--infile", "-f", type=str)
parser.add_argument("--outfile", "-o", type=str)
args = parser.parse_args()

infile = args.infile
outfile = args.outfile

filename = os.path.basename(infile)
lang = filename.split("-")[0]

def preprocess_text(source_text, lang):
    if lang == "ja":
        source_text = normalize_japanese_punct(source_text)
    elif lang == "de":
        source_text = normalize_german_punct(source_text)

    else:               
        source_text = normalize_punct(source_text)
    source_text = capitalize_after_period_space(source_text)

    return source_text

with open(infile, "r") as inf, open(outfile, "w") as outf:
    reader = csv.reader(inf)
    next(reader)
    for row in reader:
        source_text = row[1]

        source_text = preprocess_text(source_text, lang)

        json.dump({"source": source_text}, outf)
        outf.write("\n")

            



