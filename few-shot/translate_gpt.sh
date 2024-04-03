#!/bin/bash

# Need to create transaltions for the following files:

# 1. paragraph-level from ../dataprep/source_para_json
# GPT-3 for de-en_news and en-de_news
# GPT-4 for all except de-en_news and en-de_news

# 2. sentence-level from ../dataprep/source_sent_json
# GPT-3 for de-en_news and en-de_news
# GPT-4 for all

level="para" # {para, sent}
model="gpt-3.5-turbo-0125" # {gpt-4, gpt-3.5-turbo-16k}

# if model is gpt-4, then set m to gpt4, else set it to gpt3
if [ "$model" = "gpt-4" ]; then
    m="gpt4"
else
    m="gpt3"
fi

OUTDIR=translated/${level}-level

mkdir -p $OUTDIR

# model: {gpt-4, gpt-3.5-turbo-16k}
# Iterate through the files in the directory
for file in ../inputs/source_${level}_json/*.json; do
    # If "news" is not in the file name
    if [[ $file == *"_news"* ]]; then
        echo "Translating ${file}"
        

        srcL=$(basename $file | cut -d'.' -f1 | cut -d'_' -f1 | cut -d'-' -f1)
        tgtL=$(basename $file | cut -d'.' -f1 | cut -d'_' -f1 | cut -d'-' -f2)

        # Translate the file
        echo "Translating ${srcL}-${tgtL} file"
        # python3 translate_with_openAI.py \
        #     -f $file \
        #     -sl ${srcL} \
        #     -tl ${tgtL} \
        #     -p 
        #     -o $OUTDIR \
        #     -m ${model} \
        #     -l ${level} \
        #     -tmp 1 \
        #     -fp 1 \
        #     -t "w" \
        #     -c 0 # start enumerating lines from this number
    else
        srcL=$(basename $file | cut -d'.' -f1 | cut -d'-' -f1)
        tgtL=$(basename $file | cut -d'.' -f1 | cut -d'-' -f2)

        # Translate the file
        echo "Translating  ${srcL}-${tgtL} file"
        echo $srcL

        prompts_file=base_data/prompt_demonstrations_${level}.tsv

        python3 translate_with_openAI.py \
            -f $file \
            -sl ${srcL} \
            -tl ${tgtL} \
            -p $prompts_file \
            -o $OUTDIR \
            -m ${model} \
            -l ${level} \
            -tmp 1 \
            -fp 1 \
            -t "w" \
            -c 0 # start enumerating lines from this number
    fi
done
