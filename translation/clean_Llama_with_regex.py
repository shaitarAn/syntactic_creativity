# clean extra lines from Llama output

import os
import re

input_dir = "data/llama_para_txt/"
output_dir = "data/llama_para_txt_clean/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

remove_text1 = re.compile(r'translation of "(.*)".* English is "(.*)"')
remove_text5 = re.compile(r'"(.*)".*translat.*"(.*)"(.*)?')
remove_text2 = re.compile(r'text you provided, "(.+)" doesn')
remove_text3 = re.compile(r"Sure, I'd be happy to help you with that! The text you provided is in \w+,? .* translation (in|to) \w+( would be)?:")
remove_text4 = re.compile(r"The text you provided is in \w+,? .* translates to:")
remove_text6 = re.compile(r"\(?.*\b[Tt]ranslation\b.*[:\n]?.*\)?")

# remove_text7 = re.compile(r"\(Translation.*\)$")


# iterate over files in input directory
for file in os.listdir(input_dir):
    # get path to file
    file = os.path.join(input_dir, file)
    with open(file, "r") as f, open(os.path.join(output_dir, os.path.basename(file)), "w") as f_out:
        lines = f.readlines()
        for line in lines:
            if line == "\n":
                continue
            if line.startswith("(Note: "):
                continue
            line = line.strip()
            match = remove_text1.search(line)
            match2 = remove_text2.search(line)
            match5 = remove_text5.search(line)
            if match:
                line = match.group(2)
                line = line[0].upper() + line[1:]
                if line[-1] != ".":
                    line = line + "."
            if match2:
                print(line)
                line = match2.group(1)
                line = line[0].upper() + line[1:]
                line = line.strip(".,") + "."

            if match5:
                line = match5.group(2)
                line = line[0].upper() + line[1:]
                line = line.strip(".,") + "."

            # if line matches removetext3, skip it
            if remove_text3.match(line):
                continue  
            if remove_text4.match(line):
                continue 
            if remove_text6.match(line):
                continue
            # if remove_texxt7.match(line):
                # continue

            if "I cannot provide a translation of that text as it contains harmful" in line:
                continue
            if "I'm not sure what you mean by 'fly' and 'bee.' Could you please provide more context or clarify your question?" in line:
                continue

            
            f_out.write(line + "\n")


            