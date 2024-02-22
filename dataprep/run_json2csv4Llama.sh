#!/bin/bash

level="sent"

DATADIR="llama_translations/llama_${level}_json"
OUTDIR="llama_translations/llama_${level}_csv"

mkdir -p "$OUTDIR"

# echo "$DATADIR"

for input_file in "$DATADIR"/*.jsonl; do
    # Extract the desired part of the filename
    filename=$(basename "$input_file")
    # split the filename by the dot into parts
    IFS='.' read -ra langs <<< "$filename"
    # replace "_" with "-" in langs
    langs=$(echo "${langs[0]}" | tr '_' '-')
    # replace "-news" with "_news" in langs
    langs=$(echo "${langs}" | sed 's/-news/_news/g')
    output_file="${langs}.${level}.llama.csv"


    # create the output file path
    output_file="$OUTDIR/$output_file"
    echo "$output_file"

    echo "-------------------"

    python3 json2csv.py -f "$input_file" -o "$output_file"
done