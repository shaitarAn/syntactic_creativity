#!/bin/bash

persona="asmachine"

inputdir="translated/sent-level/${persona}"
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

echo $langslist

systems="gpt3"

for langs in $langslist; do

    # iterate through the systems
    for system in $systems; do

        if [[ "$persona" == "ashuman" ]]; then
                suffix="hum"
            else
                suffix="mch"
        fi

        for run in "1" "2" "3" "4" "5"; do

            parasrc="../inputs/source_para_json/${langs}.para.source.json"
            sentfile="${inputdir}/${langs}.sent.${system}.${run}.csv"

            python ../dataprep/merge_sents2paras.py -ps "$parasrc" -sf "$sentfile" -out "$outputdir" -r "$run" -s $suffix
        done

    done

done


