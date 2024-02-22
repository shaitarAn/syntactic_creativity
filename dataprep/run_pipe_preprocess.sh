#!/bin/bash

for level in "para" "sent"; do
    
    mkdir -p ../inputs/${level}s_cleaned
    
    # ####################
    # preprocess data
    
    find "../inputs/${level}s_cleaned/" -type f -name "*.txt" -exec rm -vf {} +

    python3 preprocess_texts.py -l ${level} -wd ../inputs

    echo "Done preprocessing"

    # ####################
    # align paragraphs

    cp ../inputs/paras_cleaned/*human* ../inputs/sents_cleaned
    cp ../inputs/paras_cleaned/*source* ../inputs/sents_cleaned

    cd bertalign

    python3 align_paras.py -l ${level}

    cd ..

    # ####################
    # split into sents
    
    inputdir=../inputs/${level}s_cleaned
    outputdir=../inputs/${level}s_splits
    
    mkdir -p $outputdir

    find "../inputs/${level}s_splits/" -type f -name "*.txt" -exec rm -vf {} \;

    python3 split_sents.py -i ${inputdir} -o ${outputdir}

    echo "Done splitting sentences"


done
