level="para" # {para, sent}
model="gpt-4" # {gpt-4, gpt-3.5-turbo-16k}

# if model is gpt-4, then set m to gpt4, else set it to gpt3
if [ "$model" = "gpt-4" ]; then
    m="gpt4"
else
    m="gpt3"
fi

OUTDIR=translated/${level}-level

mkdir -p $OUTDIR

prompts_file=base_data/prompt_demonstrations_${level}.tsv

python3 translate_with_openAI.py \
    -f ../inputs/source_${level}_json/en-ja.para.source.json \
    -sl "en" \
    -tl "ja" \
    -p $prompts_file \
    -o $OUTDIR \
    -m ${model} \
    -l ${level} \
    -tmp 1 \
    -fp 1 \
    -t "w" \
    -c 0 # start enumerating lines from this number