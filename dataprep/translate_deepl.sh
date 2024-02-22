#!/bin/bash

OUTDIR=deepl_translations

mkdir -p $OUTDIR

# iterate through the files in the directory
for file in source_sents_json/*json; do
    
    echo "Processing file: $file"

    tgtL=$(basename $file | cut -d'.' -f1 | cut -d'_' -f1 | cut -d'-' -f2)

    python3 translate_deepL.py \
                  -f $file \
                  -o $OUTDIR \
                  -tl $tgtL

done
