"""
iterate through directory of csv files, read each file, and write to new csv file. Remove strings that indicate error warnings from the translation column.
"""

import os
import csv
import re

level = "sent"

# input directory
input_dir = f"llama_translations/llama_{level}_llama_fixed_news"

# output directory
output_dir = f"final_csv/{level}s/llama"
os.makedirs(output_dir, exist_ok=True)

outputdir_txt = f"final_txt/{level}s/llama"
os.makedirs(outputdir_txt, exist_ok=True)

error_strings = ["WRONG STATEMENT, TRANSLATION FOUND", "INACCURATE TRANSLATION"]
# <<INACCURATE TRANSLATION>>
# <<WRONG STATEMENT, TRANSLATION FOUND. sometimes ending on : or >>

# iterate over csv files in input directory
for file in os.listdir(input_dir):
    file = os.path.join(input_dir, file)
    #  extract filename without extension
    filename = os.path.basename(file)

    with open(file, 'r') as inf, open(output_dir + "/" + filename, 'w') as outf, open(outputdir_txt + "/" + ".".join(filename.split(".")[:-1]) + ".txt", 'w') as outf_txt:
        reader = csv.reader(inf, delimiter=',', quotechar='"')
        # skip header
        next(reader)

        writer = csv.writer(outf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "source", "translation"])

        for row in reader:
            line_num = row[0]
            source = row[1]
            translation = row[2]

            # check if translation contains error string
            if any(error in translation for error in error_strings):
                for error in error_strings:
                    if error in translation:
                        # error might have a period or colon at the end
                        # remove error string together with period or colon if present
                        if error + "." in translation:
                            translation = translation.replace(error + ". ", "")
                        elif error + ">>:" in translation:
                            translation = translation.replace(error + ">>: ", "")
                        elif error + ":" in translation:
                            translation = translation.replace(error + ": ", "")
                        else:
                            translation = translation.replace(error, "")
                        # remove extra spaces on the left
                        translation = translation.lstrip()
                        # remove extra spaces on the right
                        translation = translation.rstrip()
                        # remove extra new lines
                        translation = re.sub(r"\n", " ", translation)
                        translation = translation.replace("<<", "")
                        translation = translation.replace(">>", "")
                writer.writerow([line_num, source, translation])
                outf_txt.write(translation + "\n")
            else:
                translation = re.sub(r"\n", " ", translation)
                translation = translation.strip()
                writer.writerow([line_num, source, translation])
                outf_txt.write(translation + "\n")







