#!/bin/bash

level="sent"

DATADIR="data/llama_translations/llama_${level}_json_news"
OUTDIR="data/llama_translations/llama_${level}_csv_news"

mkdir -p "$OUTDIR"

# echo "$DATADIR"

for input_file in "$DATADIR"/*.jsonl; do
    # Extract the desired part of the filename
    filename=$(basename "$input_file")
    # split the filename by the dot into parts
    IFS='.' read -ra parts <<< "$filename"
    # split the first part by the underscore into parts
    IFS='_' read -ra langs <<< "${parts[0]}"
    output_file="${langs[0]}-${langs[1]}_${langs[2]}.${level}.llama.asis.csv"

    # create the output file path
    output_file="$OUTDIR/$output_file"
    echo "$output_file"

    echo "-------------------"

    python3 json2csv.py -f "$input_file" -o "$output_file"
done