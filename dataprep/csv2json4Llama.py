import json
import argparse
import csv

# convert csv to json for Llama where each line has the following format: {"source": "Lead researchers say this may bring early detection of cancer, tuberculosis, HIV and malaria to patients in low-income countries, where the survival rates for illnesses such as breast cancer can be half those of richer countries."}

parser = argparse.ArgumentParser()
parser.add_argument("--infile", "-f", type=str)
parser.add_argument("--outfile", "-o", type=str)
args = parser.parse_args()

infile = args.infile
outfile = args.outfile

# print("infile: ", infile)

with open(infile, "r") as inf, open(outfile, "w") as outf:
    reader = csv.reader(inf)
    next(reader)
    for row in reader:
        source = row[1]
        json.dump({"source": source}, outf)
        outf.write("\n")

            



