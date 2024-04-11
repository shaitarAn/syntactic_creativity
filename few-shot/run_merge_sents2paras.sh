#!/bin/bash

inputdir="translated/sent-level"
outputdir="inputs/sents"
mkdir -p $outputdir


# initialize a list of lang pairs
langslist=""

# iterate through the files in the directory
for file in ${inputdir}/*csv; do
    
    # echo "Processing file: $file"

    langs=$(basename $file | cut -d'.' -f1 )
    # append langs to langslist
    langslist="$langslist $langs"

done

# Remove duplicates from langslist
langslist=$(echo "$langslist" | tr ' ' '\n' | sort -u | tr '\n' ' ')

systems="gpt4 gpt3"

for langs in $langslist; do

    # iterate through the systems
    for system in $systems; do

        parasrc="../inputs/source_para_json/${langs}.para.source.json"
        sentfile="${inputdir}/${langs}.sent.${system}.csv"

        python ../dataprep/merge_sents2paras.py -ps "$parasrc" -sf "$sentfile" -out "$outputdir"

    done

done


