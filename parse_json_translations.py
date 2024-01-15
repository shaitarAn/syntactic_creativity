import json
import os
import csv

""" 
Parse a json file with annotations and create text files for each book. 
Extract human preferences into a csv file.
Data is from https://github.com/marzenakrp/LiteraryTranslation
"""

def create_filename(book, suffix):
    book_name = book.replace(" ", "_")
    outdir = f'data/littrans/{book_name}'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    return os.path.join(outdir, f"{book_name}_{suffix}.txt")

def write_to_file(filename, texts):
    with open(filename, 'w', encoding='utf-8') as file:
        for text in texts:
            file.write(text + '\n')

with open('data/all_annotations_v1.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# extract book titles from json
books = {}

# initiate a list of user choices (preferences of the translations)
choices = []


for entry in json_data:
    b = entry['book']
    src = entry['source_lang']
    tgt = entry['target_lang']
    choice = entry['choice']
    book = b + "_" + src + "-" + tgt
    # print(book)
    if book not in books:
        books[book] = {"source": [], "target": [], "gpt_sent": {"txt":[], "anno":[]}, "gpt_para":{"txt":[], "anno":[]}, "gtr": {"trg": [], "src": []}}

    if entry['choice'] == "text1":
        ch = entry["text1_tag"]
    else:
        ch = entry["text2_tag"]

    choices2list = [entry["eval"], ch, entry['text1_tag'], entry['text2_tag'], entry['difficult_choice'], entry['comment'], entry['text1'], entry['text2']]
    choices.append(choices2list)

    if entry['source'] not in books[book]["source"]:
        books[book]["source"].append(entry['source'])
    if entry['target'] not in books[book]["target"]:
        books[book]["target"].append(entry['target'])
    if entry['text1'] not in books[book]["gpt_sent"]["txt"] and entry['text1_tag'] == "sent":
        books[book]["gpt_sent"]["txt"].append(entry['text1'])
        if entry['choice'] == "text1":
            books[book]["gpt_sent"]["anno"].append(entry["text1_tag"])
        else:
            books[book]["gpt_sent"]["anno"].append(entry["text2_tag"])

    if entry['text1'] not in books[book]["gpt_para"]["txt"] and entry['text1_tag'] == "para":
        books[book]["gpt_para"]["txt"].append(entry['text1'])
        if entry['choice'] == "text1":
            books[book]["gpt_para"]["anno"].append(entry["text1_tag"])
        else:
            books[book]["gpt_para"]["anno"].append(entry["text2_tag"])
    
    if entry['text1'] not in books[book]["gtr"]["trg"] and entry['text1_tag'] == "gtr":
        books[book]["gtr"]["trg"].append(entry['text1'])
        books[book]["gtr"]["src"].append(entry['source'])

    if entry['text2'] not in books[book]["gpt_sent"]["txt"] and entry['text2_tag'] == "sent":
        books[book]["gpt_sent"]["txt"].append(entry['text2'])
        if entry['choice'] == "text1":
            books[book]["gpt_sent"]["anno"].append(entry["text1_tag"])
        else:
            books[book]["gpt_sent"]["anno"].append(entry["text2_tag"])
    if entry['text2'] not in books[book]["gpt_para"]["txt"] and entry['text2_tag'] == "para":
        books[book]["gpt_para"]["txt"].append(entry['text2'])
        if entry['choice'] == "text1":
            books[book]["gpt_para"]["anno"].append(entry["text1_tag"])
        else:
            books[book]["gpt_para"]["anno"].append(entry["text2_tag"])

    if entry['text2'] not in books[book]["gtr"]["trg"] and entry['text2_tag'] == "gtr":
        books[book]["gtr"]["trg"].append(entry['text2'])
        books[book]["gtr"]["src"].append(entry['source'])       

def create_text_files():
    for book in books.keys():
        source_filename = create_filename(book, 'source')
        write_to_file(source_filename, books[book]["source"])

        target_filename = create_filename(book, 'target')
        write_to_file(target_filename, books[book]["target"])

        gpt_sent_filename = create_filename(book, 'sent')
        write_to_file(gpt_sent_filename, books[book]["gpt_sent"]["txt"])

        gpt_para_filename = create_filename(book, 'para')
        write_to_file(gpt_para_filename, books[book]["gpt_para"]["txt"])

        gtr_filename = create_filename(book, 'gtr')
        write_to_file(gtr_filename, books[book]["gtr"]["trg"])

create_text_files()
        
# write list of choices to csv file
with open('output/choices.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["eval", "choice", "text1_tag", "text2_tag", "difficult_choice", "comment", "text1", "text2"])
    writer.writerows(choices)
        



