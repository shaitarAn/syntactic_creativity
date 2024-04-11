#!/bin/bash

for level in "para" "sent"; do

    ###################
    # Calculate "n2m", "n2mR", "length_var", "merges", "splits"
    # create csv results table per level

    output_dir="../few-shot"
    
    mkdir -p ${output_dir}/output
    mkdir -p ${output_dir}/output/aligned_sentences_${level}
    mkdir -p ${output_dir}/results

    # find "${output_dir}/aligned_sentences_${level}/" -type f -name "*.csv" -exec rm -f {} \;

    # cd bertalign

    # python3 align_sents.py -l ${level} -o ${output_dir}

    # echo "Done aligning sentences for ${level}"

    # ####################
    # Perform word alignment and calculate cross word ratio (XWR)
    #  create csv results table per level

    # cd ..

    python3 xwr.py -l ${level} -i ${output_dir}

    # ####################
    # Merge results tables on the 'lang' and 'system' columns

    # python3 merge_csv.py -l ${level}

done
