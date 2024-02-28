# -*- coding: utf-8 -*-
"""
Perform word alignment and calculate cross word ratio (XWR)
"""

import torch
import os
import csv
from nltk import Alignment
import argparse
import numpy as np
# from utils import normalize_punct
from transformers import AutoModel, AutoTokenizer

os.environ['CUDA_VISIBLE_DEVICES'] = '2'

model_name = "xlm-roberta-base"
model = AutoModel.from_pretrained(model_name)

# Move the model to GPU
if torch.cuda.is_available():
    model = model.to('cuda')
else:
    print("CUDA is not available. Using CPU.")
          
tokenizer = AutoTokenizer.from_pretrained(model_name)
layer = 8

parser = argparse.ArgumentParser()
parser.add_argument("--level", "-l", type=str)
args = parser.parse_args()

level = args.level

languages = set()

# input_dir = f'data/{level}s_cleaned'
input_dir = f"../inputs/{level}s"

# Check if the directory exists, if not, create it
if not os.path.exists("../output/alignments_per_file"):
    os.makedirs("../output/alignments_per_file")

for file in os.listdir(input_dir):
  filename_parts = file.split(".")
  langs = filename_parts[0]
  system = filename_parts[2]
  languages.add(langs)

def get_subword_embeddings(paragraph: str) -> torch.Tensor:
    # If a paragraph exceeds the max length of the model, embed it in chunks and concatenate the results
    max_length = model.config.max_position_embeddings - 5
    chunk_embeddings = []
    tokens = tokenizer.tokenize(paragraph)
    for i in range(0, len(tokens), max_length):
        chunk_tokens = tokens[i:i + max_length]
        chunk_str = tokenizer.convert_tokens_to_string(chunk_tokens)
        encoding = tokenizer(chunk_str, return_tensors="pt")
        # Move encoding to GPU
        encoding = {k: v.to('cuda') for k, v in encoding.items()}  
        model_output = model(**encoding, return_dict=True, output_hidden_states=True)
        hidden_states = model_output.hidden_states[layer].squeeze(0)
        # Do not include special tokens in alignment
        hidden_states = hidden_states[1:-1]
        chunk_embeddings.append(hidden_states)
    subword_embeddings = torch.cat(chunk_embeddings)
    # print(subword_embeddings)
    return subword_embeddings

# Function to find crossed word alignments
def find_cross_algnmts(seq):
    pairs = []
    for i in range(len(seq)):
        for j in range(i+1, len(seq)):
            # Compare elements in the same position
            if seq[i][0] < seq[j][0] and seq[i][1] > seq[j][1]:
                pairs.append((seq[i], seq[j]))
            elif seq[i][0] > seq[j][0] and seq[i][1] < seq[j][1]:
                pairs.append((seq[j], seq[i]))

    return pairs

def extract_alignments(paragraph1, paragraph2):
  embeddings1 = get_subword_embeddings(paragraph1)
  embeddings2 = get_subword_embeddings(paragraph2)
  # Calculate cosine similarity matrix
  # Source: https://github.com/ZurichNLP/swissbert/blob/master/evaluation/romansh_alignment/word_aligners/simalign_aligner.py#L125
  a = embeddings1.unsqueeze(0)
  b = embeddings2.unsqueeze(0)
  eps = 1e-8
  # Initial dim: batch x seq_len x embedding_size
  a_n, b_n = a.norm(dim=2)[..., None], b.norm(dim=2)[..., None]  # Same dim
  a_norm = a / torch.max(a_n, eps * torch.ones_like(a_n))  # Same dim
  b_norm = b / torch.max(b_n, eps * torch.ones_like(b_n))
  pairwise_cosine_similarity = torch.matmul(a_norm, b_norm.transpose(1, 2))  # batch x seq_len_1 x seq_len_2
  similarity_matrix = (pairwise_cosine_similarity + 1.0) / 2.0  # Same dim

  # Calculate alignment matrix
  # Source: Source: https://github.com/ZurichNLP/swissbert/blob/master/evaluation/romansh_alignment/word_aligners/simalign_aligner.py#L140
  batch_size, seq_len_1, seq_len_2 = similarity_matrix.shape
  forward_base = torch.eye(seq_len_2, dtype=torch.bool, device=similarity_matrix.device)
  backward_base = torch.eye(seq_len_1, dtype=torch.bool, device=similarity_matrix.device)
  forward = forward_base[similarity_matrix.argmax(dim=2)]  # batch x seq_len_1 x seq_len_2
  backward = backward_base[similarity_matrix.argmax(dim=1)]  # batch x seq_len_2 x seq_len_1
  alignment_matrix = forward & backward.transpose(1, 2)

  # Turn alignment matrix into an nltk.Alignment object
  alignment_labels = alignment_matrix[0].cpu().detach().numpy()

  alignment_pairs = {tuple(pair) for pair in list(zip(*alignment_labels.nonzero()))}
  cross_pairs = find_cross_algnmts(list(alignment_pairs))

  alignment = Alignment(alignment_pairs)

  return alignment, cross_pairs

final_scores = []

for file in os.listdir(input_dir):
    lang = file.split(".")[0]
    system = file.split(".")[2]
    file = os.path.join(input_dir, file)

    xwr_list = []
    all_alignments = 0
    cross_alignments = 0

    with open(file, "r") as inf, open(f"../output/alignments_per_file/{lang}.{level}.{system}.alignments.csv", "w") as outf:
        writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "source", "translation", "alignments"])

        print(file)
        reader = csv.reader(inf, delimiter=',', quotechar='"')
        next(reader)
        
        for row in reader:
            try:
                
                alignment, cross_pairs = extract_alignments(row[1], row[2])
                writer.writerow([row[0], row[1], row[2], alignment])

                xwr_list.append(len(cross_pairs)/len(alignment)) 
                all_alignments += len(alignment)
                cross_alignments += len(cross_pairs)

            except:
                print("Could not perform alignment with SimAlign")
                print(lang)
                print(row)
                print()

    try:
        xwr_mean = np.mean(xwr_list)
        xwr_std = np.std(xwr_list)
        scores = [lang, system, all_alignments, cross_alignments, xwr_mean, xwr_std]
        final_scores.append(scores)
        print(scores)
        print("------------------------------")
    except ZeroDivisionError:
        continue


output_file = f"../results/{level}_alignment_scores.csv"


with open(output_file, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["lang", "system", "all_alignments", "cross_alignments", "xwr_mean", "xwr_std"])
    writer.writerows(final_scores)

# tokens1 = tokenizer.tokenize(paragraph1)
# tokens2 = tokenizer.tokenize(paragraph2)

# for i, j in alignment:
#   print(i,j)

#   print(tokens1[i], tokens2[j])
#   print()