#!/bin/bash

export CUDA_VISIBLE_DEVICES=1

level="para"
inputdir="one2one_only/${level}_sents"

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

# Create a CSV file to store the results
echo "lang,system,score" > comet_scores_${level}_raw.csv

for langs in $langslist; do

    echo "Processing lang pair: $langs"
    srcfile="${inputdir}/${langs}.source.txt"
    gpt3f="${inputdir}/${langs}.gpt3.txt"
    gpt4f="${inputdir}/${langs}.gpt4.txt"
    llama="${inputdir}/${langs}.llama.txt"
    human="${inputdir}/${langs}.human.txt"
    nmt="${inputdir}/${langs}.nmt.txt"

    echo "srcfile: $srcfile"
    echo "gpt3f: $gpt3f"
    echo "gpt4f: $gpt4f"
    echo "llama: $llama"
    echo "human: $nmt"
    echo "Running comet score for lang pair: $langs"

    # Check the value of the level variable
    if [[ "$level" == "sent" ]]; then
        comet-score -s "${srcfile}" -t "${gpt3f}" "${gpt4f}" "${llama}" "${nmt}"-r "${human}" --quiet --only_system >> "comet_scores_${level}_raw.csv"
    elif [[ "$level" == "para" ]]; then
        comet-score -s "${srcfile}" -t "${gpt3f}" "${gpt4f}" "${llama}" -r "${human}" --quiet --only_system >> "comet_scores_${level}_raw.csv"
    else
        echo "Invalid level. Please specify 'sentence' or 'paragraph'."
        exit 1
    fi

done

# Input and output file paths
input_file="comet_scores_${level}_raw.csv"
output_file="results/comet_scores_${level}.csv"

# Write the header line to the output file
echo "lang,system,score" > "$output_file"

# Read the input file and process each line
while read -r line; do
    # Skip the header line
    if [[ $line == "lang,system,score" ]]; then
        continue
    fi

    # Extract lang, system, and score values
    lang=$(echo "$line" | cut -d '/' -f 3 | cut -d '.' -f 1)
    system=$(echo "$line" | cut -d '.' -f 2)
    score=$(echo "$line" | awk '{print $3}')

    # Write the extracted values to the output file
    echo "$lang,$system,$score" >> "$output_file"
done < "$input_file"

rm ${input_file}
