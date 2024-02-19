#!/bin/bash

OUTDIR=/home/user/shaita/data/deepl_translations

mkdir -p $OUTDIR

# iterate through the files in the directory
for file in /home/user/shaita/data/source_sents/*; do
    
    echo "Processing file: $file"

    srcL=$(basename $file | cut -d'.' -f1 | cut -d'_' -f1 | cut -d'-' -f1)
    tgtL=$(basename $file | cut -d'.' -f1 | cut -d'_' -f1 | cut -d'-' -f2)

    python3 translate_deepL.py \
                  -f $file \
                  -o $OUTDIR \
                  -sl $srcL \
                  -tl $tgtL

done
