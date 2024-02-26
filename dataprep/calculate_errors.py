import os
import re
import csv
import json

"""
This srcipt itarates through all the files in the para and sent directories and returns the number fo different errors perf language pair.
"""

import os
import csv

level = "para"

types = ["llama_fixed", "gpt4_cleaned"]
errors = ["CORRECT STATEMENT, NO TRANSLATION FOUND", "WRONG STATEMENT, TRANSLATION FOUND", "INACCURATE TRANSLATION"]

for type in types:
    try:
        src_dir = f"data/llama_translations/llama_{level}_{type}/"
        outputfile_csv = f"data/llama_{level}_{type}_errors.csv"
        outputfile_tex = f"data/llama_{level}_{type}_errors.tex"

        # Create a dictionary to store errors for each language pair
        lang_errors = {}

                # Iterate over csv files in input directory
        for file in os.listdir(src_dir):
            file_path = os.path.join(src_dir, file)
            # Extract filename without extension
            filename = os.path.splitext(file)[0]
            # Extract language codes from filename
            lang_pair = filename.split(".")[0]
            if "_lit" in lang_pair:
                lang_pair = lang_pair.replace("_lit", "")
            if lang_pair not in lang_errors:
                lang_errors[lang_pair] = {error_type: "0" for error_type in errors}  # Initialize values as strings

            with open(file_path, 'r') as inf:
                reader = csv.reader(inf, delimiter=',', quotechar='"')
                # Skip header
                next(reader)
                for row in reader:
                    translation = row[2]
                    for error_type in errors:
                        if error_type in translation:
                            lang_errors[lang_pair][error_type] = str(int(lang_errors[lang_pair][error_type]) + 1)  # Convert to int, add 1, then convert back to str


        # Separate _news and non-_news language pairs
        news_lang_pairs = [lang_pair for lang_pair in lang_errors if lang_pair.endswith("_news")]
        non_news_lang_pairs = [lang_pair for lang_pair in lang_errors if not lang_pair.endswith("_news")]

        # Sort both groups alphabetically
        news_lang_pairs.sort()
        non_news_lang_pairs.sort()

        # Combine the sorted groups
        sorted_lang_pairs = non_news_lang_pairs + news_lang_pairs

        # Transpose the table
        transposed_table = []
        transposed_table.append([""] + sorted_lang_pairs)
        for error_type in errors:
            transposed_table_row = [error_type]
            for lang_pair in sorted_lang_pairs:
                transposed_table_row.append(lang_errors[lang_pair][error_type])
            transposed_table.append(transposed_table_row)

        # Write transposed table to CSV
        with open(outputfile_csv, "w", newline='') as outf:
            writer = csv.writer(outf)
            writer.writerows(transposed_table)

        # Convert CSV to LaTeX table format
        with open(outputfile_tex, "w") as outf:
            # Write LaTeX table preamble
            outf.write("\\begin{table*}[ht]\n")
            outf.write("\\centering\n")
            outf.write("\\small % Reduce font size\n")
            outf.write("\\begin{adjustbox}{width=\\textwidth} % Adjust table size to fit on the page\n")
            outf.write("\\begin{tabular}{l|" + "c" * len(transposed_table[0]) + "}\n")
            outf.write("\\toprule\n")
            # Write header row
            header = transposed_table[0]
            outf.write(" & \\rotatebox[origin=c]{90}{" + "} & \\rotatebox[origin=c]{90}{" .join(header[1:]) + "} \\\\\n")
            outf.write("\\midrule\n")
            # Write data rows
            for row in transposed_table[1:]:
                outf.write(" & ".join(row) + " \\\\\n")
            # Write LaTeX table closing tags
            outf.write("\\bottomrule\n")
            outf.write("\\end{tabular}\n")
            outf.write("\\end{adjustbox}\n")
            outf.write("\\caption{Error types for each language pair}\n")
            outf.write("\\label{tab:errors}\n")
            outf.write("\\end{table*}\n")

    except Exception as e:
        print(f"Error processing {type}: {e}")











