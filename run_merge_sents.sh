#!/bin/bash

inputdir="data/sents"

# initialize a list of lang pairs
langslist=""

# iterate through the files in the directory
for file in ${inputdir}/*; do
    
    # echo "Processing file: $file"

    langs=$(basename $file | cut -d'.' -f1 )
    # append langs to langslist
    langslist="$langslist $langs"

done

# Remove duplicates from langslist
langslist=$(echo "$langslist" | tr ' ' '\n' | sort -u | tr '\n' ' ')

systems="gpt4 llama"

for langs in $langslist; do

    # iterate through the systems
    for system in $systems; do

        parasrc="/home/user/shaita/data_old/paras/${langs}.para.source.asis.txt"
        senssrc="/home/user/shaita/data_old/sents/${langs}.sent.source.split.txt"
        senttgt="/home/user/shaita/data_old/sents/${langs}.sent.${system}.asis.txt"

        # merge the sentences
        python align_sents_and_parasrc.py -ps $parasrc -ss $senssrc -st $senttgt

    done

done
