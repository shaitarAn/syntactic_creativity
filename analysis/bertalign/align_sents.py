from bertalign import Bertalign
import os
import re
import torch
import json
import csv
import argparse
from transformers import BertTokenizer 

"""
Aligns sentences and calculates "n2m", "n2mR", "length_var", "merges", "splits"
"""
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

os.environ['CUDA_VISIBLE_DEVICES'] = '2'

parser = argparse.ArgumentParser()
parser.add_argument("--level", "-l", type=str, required=True, help='provide "sent" or "para"')
parser.add_argument("--output_dir", "-o", type=str, required=True)
args = parser.parse_args()

level = args.level
output_dir = args.output_dir

languages = set()

input_dir = f'../../inputs/target_sent_json_{level}-level'

output_dir = f"../{output_dir}/output/aligned_sentences_{level}"
os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
  filename_parts = file.split(".")
  langs = filename_parts[0]
  system = filename_parts[2]
  languages.add(langs)

def calculate_length_variety(src_sent, tgt_sent):
    
    tokenized_src = tokenizer.tokenize("[CLS] " + src_sent + " [SEP]")
    tokenized_tgt = tokenizer.tokenize("[CLS] " + tgt_sent + " [SEP]")

    src_len = len(tokenized_src)
    tgt_len = len(tokenized_tgt)

    len_var = abs(src_len - tgt_len) / src_len

    return len_var


final_scores = []

for lang in languages:
    print("***********")
    print(lang)

    source_file = os.path.join('../../inputs/source_sent_json', lang+f".sent.source.json")
    with open(source_file, "r") as srcF:
        source_text = [json.loads(s)["source"] for s in srcF.readlines()]
        # print(source_text)

        try:

            for file in os.listdir(input_dir):
                system = file.split(".")[2]
                langs = file.split(".")[0]
                if langs == lang and "source" not in file:
                    target_file = os.path.join(input_dir, file)

                    print(system)

                    csvfile = ".".join([langs, level, system, "csv"])
                    output_file = os.path.join(output_dir, csvfile)

                    count_n2m = 0
                    merges = 0
                    splits = 0
                    count_lines = 0
                    length_var = 0

                    slines = 0

                    with open(target_file, "r") as tgtF, open(output_file, "w", newline='') as outF:
                        target_text = [json.loads(t)["translation"] for t in tgtF.readlines()]

                        writer = csv.writer(outF, quotechar = '"')
                        writer.writerow(["id", "source", "translation", "n2m"])

                        aligner = Bertalign("\n".join(source_text), "\n".join(target_text))  
                        aligner.align_sents()

                        for bead in aligner.result:
                            
                            n2m = f"{len(bead[0])}-{len(bead[1])}"
                            count_lines += 1
                            src_line = aligner._get_line(bead[0], aligner.src_sents)
                            tgt_line = aligner._get_line(bead[1], aligner.tgt_sents)

                            # Skip the iteration if either source or target line is empty
                            if not src_line.strip() or not tgt_line.strip() or len(src_line.strip()) == 0 or len(tgt_line.strip()) == 0:
                                # print("src_line", src_line)
                                # print("tgt_line", tgt_line)
                                # print()
                                continue
                            
                            slines += 1

                            # Count n-to-m alignments
                            if len(bead[0]) != len(bead[1]):
                                count_n2m += 1
                            else:
                                length_var += calculate_length_variety(src_line, tgt_line)
                                
                            if len(bead[0]) > len(bead[1]):
                                merges += 1
                            elif len(bead[0]) < len(bead[1]):
                                splits += 1
                            
                            writer.writerow([count_lines, src_line, tgt_line, n2m])

                            

                    final_scores.append([langs, system, slines, count_n2m, count_n2m/slines, length_var/slines, merges, splits, merges/slines, splits/slines])

        except Exception as e:
            print(e)

with open(f"${output_dir}/results/{level}_n2m_scores.csv", "w") as outf:
    writer = csv.writer(outf)
    writer.writerow(["lang", "system", "total_src_sents", "n2m", "n2mR", "length_var", "merges", "splits", "mergesRatio", "splitsRatio"])
    for score in final_scores:
        writer.writerow(score)

    