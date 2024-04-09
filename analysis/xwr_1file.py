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

os.environ['CUDA_VISIBLE_DEVICES'] = '7'

model_name = "xlm-roberta-base"
model = AutoModel.from_pretrained(model_name)

# Move the model to GPU
if torch.cuda.is_available():
    model = model.to('cuda')
else:
    print("CUDA is not available. Using CPU.")
          
tokenizer = AutoTokenizer.from_pretrained(model_name)
layer = 8

languages = set()

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

inputdir = "../dataprep/par3/"
output_file = "../results/par3_xwr.csv"

with open(output_file, "w") as outf:
    writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["source_lang", "book", "GT", "human1", "human2", "human3", "human4"])

    for subdir in os.listdir(inputdir):
        lang = subdir
        for infile in os.listdir(os.path.join(inputdir, subdir)):
            print(infile)
            inputfile = os.path.join(inputdir, subdir, infile)
            book = os.path.basename(infile).replace(".csv", "")    

            with open(inputfile, "r") as inf:

                reader = csv.reader(inf, delimiter=',', quotechar='"')
                next(reader)
                
                for row in reader:
                    try:
                    
                        gtalignment, gtcross_pairs = extract_alignments(row[0], row[1])
                        gt_xwr = len(gtcross_pairs)/len(gtalignment)
                        try:
                            h1alignment, h1cross_pairs = extract_alignments(row[0], row[2])
                            h1_xwr = len(h1cross_pairs)/len(h1alignment)
                        except:
                            h1_xwr = None

                        try:
                            h2alignment, h2cross_pairs = extract_alignments(row[0], row[3])
                            h2_xwr = len(h2cross_pairs)/len(h2alignment)
                        except:
                            h2_xwr = None 

                        try:                       
                            h3alignment, h3cross_pairs = extract_alignments(row[0], row[4])
                            h3_xwr = len(h3cross_pairs)/len(h3alignment)
                        except:
                            h3_xwr = None
                            
                        try:                       
                            h4alignment, h4cross_pairs = extract_alignments(row[0], row[5])
                            h4_xwr = len(h4cross_pairs)/len(h4alignment)
                        except:
                            h4_xwr = None
                        writer.writerow([lang, book, gt_xwr, h1_xwr, h2_xwr, h3_xwr, h4_xwr])
                        
                    except:
                        print("Could not perform alignment with SimAlign")
                        print(lang, book)
                        print(row)
                        print()