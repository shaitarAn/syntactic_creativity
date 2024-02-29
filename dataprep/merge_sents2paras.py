"""
merge the target sentences into pargraphs by aligning them 
with the source paragrasphs via source sentences
Source sentences are preprocessed, but source paragraphs are not
"""

import os
import csv
import json
import argparse
import re
from utils import *

parser = argparse.ArgumentParser(description='Merge the target sentences into pargraphs by aligning them with the source paragrasphs')

parser.add_argument('-ps', '--parasrc', required=True, help='source file with paragraph segments')  
parser.add_argument('-sf', '--sentfile', required=True, help='source file with sentence segments')
parser.add_argument('-out', '--output', required=True, help='output file')

args = parser.parse_args()

parasrc = args.parasrc
sentfile = args.sentfile
outputdir = args.output

if "_news" in sentfile:
    langs = sentfile.split("_")[0]
else:
    langs = sentfile.split(".")[0]

# Define the pattern for matching (PERSON#)
person_pattern = re.compile(r'[\[\(]?PERSON\d\d*[\)\]]?')

def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()
    
def read_csv(sentfile):
    source_text = []
    target_text = []
    with open(sentfile, "r") as inf:
        reader = csv.reader(inf, delimiter=',', quotechar='"')
        next(reader)  # Skip the header row
        for row in reader:
            source_text.append(row[1])
            target_text.append(row[2])

    return source_text, target_text
    
def write_to_file(filename, texts):
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "source", "translation"])
        counter = 0
        for para, merge in texts:
            if para.strip() == "" or merge.strip() == "":
                continue
            merge = re.sub(r'\s+', ' ', merge)
            para = re.sub(r'\s+', ' ', para)
            para = re.sub(r"\.\.", ".", para)
            para = re.sub(r"\.\.+", "...", para)
            counter += 1
            writer.writerow([counter, para, merge])

def align_sents_and_parasrc(parasrc, sentfile):
    parasrc = read_file(parasrc)
    sentsrc, senttgt = read_csv(sentfile)

    grouped_sens = []
    paragraphs = []

    for para in parasrc:
        # read json data
        lang = langs.split("-")[0]
        para = json.loads(para)["source"].strip()
        para = preprocess_text(para, lang)
        para_no_persons = re.sub(person_pattern, '', para)

        para_sens = []  # Use a list to store sentences for each paragraph
        sent_gen = zip(sentsrc, senttgt)  # Create a generator for zipped sentences
        print()
        print("-------------------")
        print("para: ", para)
        print()
        for s, t in sent_gen:
            # print(s)
            s = remove_mt_artifacts(s)
            # t = remove_mt_artifacts(t)

            if langs in ["en-de_news", "de-en_news"] and len(s.split( )) == 1 or t.strip() in ['"Ich bin ein Maschinenübersetzungssystem, das Sätze aus dem Englischen ins Deutsche übersetzt. Ich antworte nur mit der Übersetzung, ohne zusätzliche Kommentare."', '"Ich bin ein Machine-Translation-System, das Sätze von Englisch nach Deutsch übersetzt. Ich antworte nur mit der Übersetzung, ohne zusätzliche Kommentare."', '"Ich bin ein maschinelles Übersetzungssystem, das Sätze aus dem Englischen ins Deutsche übersetzt."', '"Ich bin ein maschinelles Übersetzungssystem, das Sätze von Englisch nach Deutsch übersetzt. Ich antworte nur mit der Übersetzung, ohne zusätzliche Kommentare."']:
                para_no_persons = para_no_persons.replace(s, "")
                continue
            # if s.strip() matches the person_pattern, skip line
            elif re.match(person_pattern, s.strip()):
                para_no_persons = para_no_persons.replace(s, "")
                continue

            elif s.strip() in para:
                print(s)
                t = remove_mt_artifacts(t)
                # t = remove_html_chars(t)
                t = re.sub(person_pattern, '', t)
                t = re.sub(r"\.\.", ".", t)
                t = re.sub(r"\.\.+", "...", t)

                para_sens.append(t.strip())  # Add sentence to list
                

                # Remove the matched sentence from senssrc
                para = para.replace(s.strip(), '', 1)

        paragraphs.append(para_no_persons)
        para_sens = " ".join(para_sens)
        grouped_sens.append(para_sens)
        # print("-------------------------------")

    return zip(paragraphs, grouped_sens)


grouped_sens = align_sents_and_parasrc(parasrc, sentfile)

# write the merged paragraphs to a file
nameparts = os.path.basename(sentfile).split(".")
output = ".".join(nameparts[0:3]) + ".merged.csv"
output = os.path.join(outputdir, output)
write_to_file(output, grouped_sens)
