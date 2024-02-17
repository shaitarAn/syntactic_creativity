import json
import os
import csv

""" 
Parse a json file with annotations and create text files for each book. 
Extract human preferences into a csv file.
Data is from https://github.com/marzenakrp/LiteraryTranslation
"""

output_dir = "all_csv"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def write_to_file(filename, paragraphs):
    outputfile = os.path.join(output_dir, filename)
    with open(outputfile, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "source", "target"])
        count = 0
        for s, t in zip(paragraphs["src"], paragraphs["tgt"]):
            count += 1
            writer.writerow([count, s.replace("\n", ""), t.replace("\n", "")])

with open('all_annotations_v1.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

books = {}

# initiate a list of user choices (preferences of the translations)
choices = []


for entry in json_data:
    if entry["eval"][-1] == "3":
        continue
    b = entry['book']
    src = entry['source_lang']
    tgt = entry['target_lang']
    choice = entry['choice']
    book = src + "-" + tgt

    if book not in books:
        books[book] = {"gpt_sent":{"src":[], "tgt":[]}, "gpt_para":{"src":[], "tgt":[]}, "gtr":{"src":[], "tgt":[]}, "human": {"src":[], "tgt":[]}}

    if choice == "text1":
        choiceLabel = entry["text1_tag"]
        choiceText = entry["text1"]
        rejectLabel = entry["text2_tag"]
        rejectText = entry["text2"]
    else:
        choiceLabel = entry["text2_tag"]
        choiceText = entry["text2"]
        rejectLabel = entry["text1_tag"]
        rejectText = entry["text1"]

    choices2list = [entry["eval"], entry["source"].replace("\n", ""), choiceLabel, choiceText.replace("\n", ""), rejectLabel, rejectText.replace("\n", ""), entry['difficult_choice'], entry['comment']]
    choices.append(choices2list)
    
    if entry['text1'] not in books[book]["gpt_sent"]["tgt"] and entry['text1_tag'] == "sent":
        books[book]["gpt_sent"]["tgt"].append(entry['text1'])
        books[book]["gpt_sent"]["src"].append(entry['source'])
        books[book]["human"]["tgt"].append(entry['target'])
        books[book]["human"]["src"].append(entry['source'])
        
    if entry['text1'] not in books[book]["gpt_para"]["tgt"] and entry['text1_tag'] == "para":
        books[book]["gpt_para"]["tgt"].append(entry['text1'])
        books[book]["gpt_para"]["src"].append(entry['source'])
        books[book]["human"]["tgt"].append(entry['target'])
        books[book]["human"]["src"].append(entry['source'])

    if entry['text1'] not in books[book]["gtr"]["tgt"] and entry['text1_tag'] == "gtr":
        books[book]["gtr"]["tgt"].append(entry['text1'])
        books[book]["gtr"]["src"].append(entry['source'])
        books[book]["human"]["tgt"].append(entry['target'])
        books[book]["human"]["src"].append(entry['source'])

    if entry['text2'] not in books[book]["gpt_sent"]["tgt"] and entry['text2_tag'] == "sent":
        books[book]["gpt_sent"]["tgt"].append(entry['text2'])
        books[book]["gpt_sent"]["src"].append(entry['source'])


    if entry['text2'] not in books[book]["gpt_para"]["tgt"] and entry['text2_tag'] == "para":
        books[book]["gpt_para"]["tgt"].append(entry['text2'])
        books[book]["gpt_para"]["src"].append(entry['source'])

    if entry['text2'] not in books[book]["gtr"]["tgt"] and entry['text2_tag'] == "gtr":
        books[book]["gtr"]["tgt"].append(entry['text2'])
        books[book]["gtr"]["src"].append(entry['source'])

def create_csv_files():
    for book in books.keys():
        source_filename = book + ".para.human.csv"
        write_to_file(source_filename, books[book]["human"])

        source_filename = book + ".para.gpt3.csv"
        write_to_file(source_filename, books[book]["gpt_para"])

        source_filename = book + ".sent.gpt3.csv"
        write_to_file(source_filename, books[book]["gpt_sent"])

        source_filename = book + ".sent.nmt.csv"
        write_to_file(source_filename, books[book]["gtr"])

create_csv_files()
        
# make output directory
if not os.path.exists('output'):
    os.makedirs('output')
    
with open('output/littrans_annotators_choices.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["annotator", "source", "choiceLabel", "choiceText", "rejectLabel", "rejectText", "difficult_choice", "comment"])
    writer.writerows(choices)


