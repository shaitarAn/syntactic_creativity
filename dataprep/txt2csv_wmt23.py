import os
import csv

"""
This script is used to convert the WMT23 txt files to csv files. merging the source and target languages into one file."""

# Create a directory to store the csv files
output_dir = 'all_csv'
if not os.path.exists('all_csv'):
    os.makedirs('all_csv')

for lang in ["de-en", "en-de"]:

    for file in os.listdir('wmt23'):
        src_file = f'wmt23/{lang}.src.txt'
        sys = file.split('.')[-2]

        if sys == "human":
            tgt_file = f'wmt23/{lang}.human.txt'
            output_file = f'{output_dir}/{lang}_news.para.human.csv'
        elif sys == "GPT4-5shot":
            tgt_file = f'wmt23/{lang}.hyp.GPT4-5shot.txt'
            output_file = f'{output_dir}/{lang}_news.para.gpt4.csv'
        elif sys == "ONLINE-A" and lang == "de-en":
            tgt_file = f'wmt23/{lang}.hyp.ONLINE-A.txt'
            output_file = f'{output_dir}/{lang}_news.sent.nmt.csv'
        elif sys == "ONLINE-B" and lang == "en-de":
            tgt_file = f'wmt23/{lang}.hyp.ONLINE-B.txt'
            output_file = f'{output_dir}/{lang}_news.sent.nmt.csv'
        else:
            continue

        with open(src_file, 'r') as src, open(tgt_file, 'r') as tgt, open(output_file, 'w') as out:
            src_lines = src.readlines()
            tgt_lines = tgt.readlines()
            writer = csv.writer(out)
            count = 0
            writer.writerow(["id", "source", "target"])
            for src_line, tgt_line in zip(src_lines, tgt_lines):
                count += 1
                writer.writerow([count, src_line.strip().replace("\n", ""), tgt_line.strip().replace("\n", "")])
   
    
