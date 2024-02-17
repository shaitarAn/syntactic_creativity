#!/bin/bash

INPUTDIR=output/paragraph-level

# iterate over all files in the input directory
for file in $INPUTDIR/*.csv

do
    # if "fixed" not in the filename 
    # and "gpt" is in filename, then postprocess the translations
    if [[ $file != *"fixed"* ]] && [[ $file == *"gpt"* ]]; then
        echo $file
        python3 postprocess_gpt_translations.py \
                  -f $file \
                  -tmp 1 \
                  -fp 1
    fi
done

