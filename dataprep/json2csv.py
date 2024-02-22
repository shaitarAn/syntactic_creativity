import os
import csv
import sys
import json
import argparse

"""
Convert json files to csv files
"""

parser = argparse.ArgumentParser(description='Convert a json file to a csv file.')
parser.add_argument('-f', '--infile', required=True, help='the file to be converted')
parser.add_argument('-o', '--outfile', required=True, help='the output file of the converted file.')
args = parser.parse_args()

infile = args.infile
outfile = args.outfile

count = 0

with open(infile, "r") as inf, open(outfile, "w") as outf:
    writer = csv.writer(outf)
    writer.writerow(["id", "source", "translation"])
    for line in inf:
        count += 1
        data = json.loads(line)
        writer.writerow([count, data["source"], data["system"]])

