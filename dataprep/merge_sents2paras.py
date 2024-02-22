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

args = parser.parse_args()

parasrc = args.parasrc
sentfile = args.sentfile

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
        writer.writerow(["id", "source", "target"])
        counter = 0
        for para, merge in texts:
            para = json.loads(para)["source"].strip()
            counter += 1
            writer.writerow([counter, para, merge])

            

def clean_text(text):
    text = text.replace("Sorry, but I am unable to translate an unintelligible text. If you provide a clear text in English, I will be happy to help you with the translation into German.", "<unintelligible>") # 4 occurences in de-en gpt3
    text = text.replace("Translate the following text into de. Output only the translation itself without additional commentary or explanations. Text: ", "") # 68 occurences in en-de_news.gpt3!
    text = text.replace("Translate the following text into de. Output only the translation itself without additional commentary or explanations.  Text: ", "")
    text = text.replace("Could you please provide the text you want me to translate?", "") # 1 time in en-de gpt4
    text = text.replace("As a translator, I need the text to be translated. Currently, the text """, "")
    text = text.replace('"" is not providing any content to be translated to German. Please provide the necessary details.', "") # 8 occurences de-en gpt4 for sentences like (PERSON#)
    text = text.replace("You need to provide a text for translation.", "(PERSON1)")
    text = text.replace("Could you please provide the text you want me to translate?", "1)")
    text = text.replace("The target text includes a German translation of the source text. The German translation is: ", "")
    text = text.replace("The German translation of the source text is:", "")
    text = text.replace("The text translates to: ", "")
    text = text.replace("The text you provided (""1"") does not need to be translated as it is a numeral, which stays the same in both German (de) and English (en).", "1")
    text = text.replace("\n", "")
    
    return text


# Define the pattern for matching (PERSON#)
person_pattern = re.compile(r'^\(PERSON\d+\)$')

def align_sents_and_parasrc(parasrc, sentfile):
    parasrc = read_file(parasrc)
    senssrc, senttgt = read_csv(sentfile)

    grouped_sens = []

    for para in parasrc:
        # read json data
        para = json.loads(para)["source"].strip()

        print("para: ", para)

        para_sens = []  # Use a list to store sentences for each paragraph
        sent_gen = zip(senssrc, senttgt)  # Create a generator for zipped sentences
        # print(para)
        for s, t in sent_gen:
            s = clean_text(s)
            t = clean_text(t)
            if s.strip() in para:
                # print("+++", s,t)
                if person_pattern.match(s.strip()):  # Check if s matches (PERSON#)
                    t = s  
                if t == """Ich bin ein Machine-Translation-System, das Sätze von Englisch nach Deutsch übersetzt. Ich antworte nur mit der Übersetzung, ohne zusätzliche Kommentare.""":
                    t = s
                # Set t to be equal to s
                # t = clean_text(t)
                para_sens.append(t.strip())  # Add sentence to list
                # print("para: ", para)
                # print(s)
                # print("*")
                # Remove the matched sentence from senssrc
                para = para.replace(s.strip(), '', 1)

        para_sens = " ".join(para_sens)
        grouped_sens.append(para_sens)
        # print("-------------------------------")

    return zip(parasrc, grouped_sens)


grouped_sens = align_sents_and_parasrc(parasrc, sentfile)

# write the merged paragraphs to a file
nameparts = os.path.basename(sentfile).split(".")
output = ".".join(nameparts[0:3]) + ".merged.csv"
output = os.path.join("merged", output)
write_to_file(output, grouped_sens)