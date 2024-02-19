#!/bin/bash


DATADIR="all_csv"
OUTDIR="source_para_json"

mkdir -p "$OUTDIR"

# echo "$DATADIR"

for input_file in "$DATADIR"/*human.csv; do
    # Extract the desired part of the filename
    filename=$(basename "$input_file")
    # echo "$filename"
    # change the extension of the filename to remove "human.csv" and replace it with "json"
    output_file="${filename/human.csv/source.json}"

    # create the output file path
    output_file="$OUTDIR/$output_file"
    echo "$output_file"

    echo "-------------------"

    python3 csv2json4Llama.py -f "$input_file" -o "$output_file"
done


