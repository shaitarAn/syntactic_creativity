import os
import csv

level = "sent"

inputdir = f"../output/aligned_sentences_{level}"
outputdir = f"one2one_only/{level}_sents"

languages = set()

if level == "sent": 
    systems = ['gpt3', 'gpt4', 'llama', 'nmt']
else:
    systems = ['gpt3', 'gpt4', 'llama']

# Extract language pairs
for file in os.listdir(inputdir):
    langs = file.split(".")[0]
    languages.add(langs)

for lang in languages:
    print("Processing:", lang)
    source_human_dict = {}
    source_gpt3_dict = {}
    source_gpt4_dict = {}
    source_llama_dict = {}
    source_nmt_dict = {}

    # Open the human translations file and read the sentences into a dictionary
    human_file = os.path.join("../output/aligned_sentences_para", f"{lang}.para.human.csv")
    with open(human_file, 'r') as inf:
        reader = csv.reader(inf)
        next(reader)  # Skip header
        for row in reader:
            if row[3] == "1-1":
                source_human_dict[row[1]] = row[2]

    # Process each system translation file
    for system in systems:
        system_file = os.path.join(inputdir, f"{lang}.{level}.{system}.csv")
        with open(system_file, 'r') as inf:
            reader = csv.reader(inf)
            next(reader)  # Skip header
            for row in reader:
                if row[3] == "1-1":
                    if system == 'gpt3':
                        source_gpt3_dict[row[1]] = row[2]
                    elif system == 'gpt4':
                        source_gpt4_dict[row[1]] = row[2]
                    elif system == 'llama':
                        source_llama_dict[row[1]] = row[2]
                    elif system == 'nmt':
                        source_nmt_dict[row[1]] = row[2]

    # Find the intersection of source sentences across all dictionaries                        
    if level == "sent":
        intersection_sources = set(source_human_dict.keys()) & set(source_gpt3_dict.keys()) & set(source_gpt4_dict.keys()) & set(source_llama_dict.keys() & set(source_nmt_dict.keys()))
    else:
        intersection_sources = set(source_human_dict.keys()) & set(source_gpt3_dict.keys()) & set(source_gpt4_dict.keys()) & set(source_llama_dict.keys())

    # Write the intersected sentences to their respective files
    src_filename = f"one2one_only/{level}_sents/{lang}.source.txt"
    ref_filename = f"one2one_only/{level}_sents/{lang}.human.txt"
    os.makedirs(os.path.dirname(src_filename), exist_ok=True)

    with open(src_filename, 'w') as src_file, open(ref_filename, 'w') as ref_file:
        for source in intersection_sources:
            src_file.write(source + "\n")
            ref_file.write(source_human_dict[source] + "\n")

    for system in systems:
        system_filename = f"one2one_only/{level}_sents/{lang}.{system}.txt"
        with open(system_filename, 'w') as sys_file:
            if system == 'gpt3':
                for source in intersection_sources:
                    sys_file.write(source_gpt3_dict[source] + "\n")
            elif system == 'gpt4':
                for source in intersection_sources:
                    sys_file.write(source_gpt4_dict[source] + "\n")
            elif system == 'llama':
                for source in intersection_sources:
                    sys_file.write(source_llama_dict[source] + "\n")
            elif system == 'nmt':
                for source in intersection_sources:
                    sys_file.write(source_nmt_dict[source] + "\n")
