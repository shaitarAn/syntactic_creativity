#!/bin/bash

inputdir="news_to_align"

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

systems="llama gpt4 gpt3"

for langs in $langslist; do

    # iterate through the systems
    for system in $systems; do

        parasrc="inputs/paras_cleaned/${langs}.para.source.asis.txt"
        llamafile="/home/user/shaita/news_to_merge/${langs}.sent.${system}.csv"

        # merge the sentences
        python merge_llama_news.py -ps $parasrc -lf $llamafile

    done

done
