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
            writer.writerow([count, s.replace("\n", " "), t.replace("\n", " ")])

with open('all_annotations_v1.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

books = {}

# initiate a list of user choices (preferences of the translations)
choices = []

source_paras = []

for entry in json_data:
    if entry["eval"][-1] == "2":
        continue

    b = entry['book']
    src = entry['source_lang']
    tgt = entry['target_lang']
    book = f"{src}-{tgt}"

    if entry['choice'] == "text1":
        ch = entry["text1_tag"]
    else:
        ch = entry["text2_tag"]

    if book not in books:
        books[book] = {"human": {"src": [], "tgt": []}, "gpt_sent": {"src": [], "tgt": []}, "gpt_para": {"src": [], "tgt": []}, "nmt": {"src": [], "tgt": []}}

    choices2list = [entry["eval"], ch, entry['text1_tag'], entry['text2_tag'], entry['difficult_choice'], entry['comment'], entry['text1'], entry['text2']]
    choices.append(choices2list)

    if entry['source'] not in books[book]["human"]["src"]:
        books[book]["human"]["src"].append(entry['source'])
    if entry['target'] not in books[book]["human"]["tgt"]:
        books[book]["human"]["tgt"].append(entry['target'])

    if entry['text1'] not in books[book]["gpt_sent"]["tgt"] and entry['text1_tag'] == "sent":
        books[book]["gpt_sent"]["tgt"].append(entry['text1'])
        books[book]["gpt_sent"]["src"].append(entry['source'])

    if entry['text1'] not in books[book]["gpt_para"]["tgt"] and entry['text1_tag'] == "para":
        books[book]["gpt_para"]["tgt"].append(entry['text1'])
        books[book]["gpt_para"]["src"].append(entry['source'])

    if entry['text1'] not in books[book]["nmt"]["tgt"] and entry['text1_tag'] == "gtr":
        books[book]["nmt"]["tgt"].append(entry['text1'])
        books[book]["nmt"]["src"].append(entry['source'])

    if entry['text2'] not in books[book]["gpt_sent"]["tgt"] and entry['text2_tag'] == "sent":
        books[book]["gpt_sent"]["tgt"].append(entry['text2'])
        books[book]["gpt_sent"]["src"].append(entry['source'])

    if entry['text2'] not in books[book]["gpt_para"]["tgt"] and entry['text2_tag'] == "para":
        books[book]["gpt_para"]["tgt"].append(entry['text2'])
        books[book]["gpt_para"]["src"].append(entry['source'])

    if entry['text2'] not in books[book]["nmt"]["tgt"] and entry['text2_tag'] == "gtr":
        books[book]["nmt"]["tgt"].append(entry['text2'])
        books[book]["nmt"]["src"].append(entry['source'])        
            

# reorder the data to make sure that the nmt paras are in the same order as the human paras
for book in books.keys():
    human_src = books[book]["human"]["src"]
    human_tgt = books[book]["human"]["tgt"]
    new_nmt_src = []
    new_nmt_tgt = []

    for s, t in zip(human_src, human_tgt):
        if s in books[book]["nmt"]["src"]:
            idx = books[book]["nmt"]["src"].index(s)
            new_nmt_src.append(s)
            new_nmt_tgt.append(books[book]["nmt"]["tgt"][idx])
        else:
            new_nmt_src.append(s)
            new_nmt_tgt.append("")

    books[book]["nmt"]["src"] = new_nmt_src
    books[book]["nmt"]["tgt"] = new_nmt_tgt

def create_csv_files():
    for book in books.keys():
        source_filename = book + ".para.human.csv"
        write_to_file(source_filename, books[book]["human"])

        source_filename = book + ".para.gpt3.csv"
        write_to_file(source_filename, books[book]["gpt_para"])

        source_filename = book + ".sent.gpt3.csv"
        write_to_file(source_filename, books[book]["gpt_sent"])

        source_filename = book + ".sent.nmt.csv"
        write_to_file(source_filename, books[book]["nmt"])

create_csv_files()
        
# make output directory
if not os.path.exists('output'):
    os.makedirs('output')
    
with open('output/littrans_annotators_choices.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["annotator", "source", "choiceLabel", "choiceText", "rejectLabel", "rejectText", "difficult_choice", "comment"])
    writer.writerows(choices)


