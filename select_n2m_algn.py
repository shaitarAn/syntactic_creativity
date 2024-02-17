import os
import csv
import pandas as pd

levels = ["para", "sent"]

all_alignments = 0
all_n2ms = 0
all_merges = 0
all_sent_merges = 0

for level in levels:
    inputdir = f"aligned_sentences_{level}"
    outputdir = f"data/n2m_only/{level}_sents"
    os.makedirs(outputdir, exist_ok=True)

    level_alignments = 0
    level_n2ms = 0
    level_merges = 0

    all_langs_file = f"data/n2m_only/{level}_sents/all_langs_{level}.csv"
    with open(all_langs_file, 'w') as outf:
        writerA = csv.writer(outf)
        writerA.writerow(["langs", "system", "n2m", "source", "target", "n2mS", "n2mT"])
        # Extract language pairs and system
        for file in os.listdir(inputdir):
            filepath = os.path.join(inputdir, file)
            filename = os.path.basename(file)
            langs, _, system, _ = filename.split(".")
            
            count_n2ms = 0

            with open(filepath, 'r') as inf, open(os.path.join(outputdir, filename), 'w') as outf:
                reader = csv.reader(inf)
                next(reader)  # Skip header
                writer = csv.writer(outf)
                writer.writerow(["id", "source", "target", "n2m"])

                for row in reader:
                    level_alignments += 1
                    all_alignments += 1
                    n2m = row[3]
                    n2ms = n2m.split("-")[0]
                    n2mt = n2m.split("-")[1]
                    if n2m.split("-")[0] != n2m.split("-")[1]:
                        count_n2ms += 1
                        level_n2ms += 1
                        all_n2ms += 1
                        writer.writerow(row)
                        writerA.writerow([langs, system, n2m, row[1], row[2], n2ms, n2mt])
                    if n2ms > n2mt:
                        level_merges += 1
                        all_merges += 1


    if level == "sent":
        all_sent_merges = level_merges
    print(f"{level} alignments: \t\t{level_alignments}")
    print(f"{level} n2m alignments: \t\t{level_n2ms}")
    print(f"{level} percentage of n2m: \t{level_n2ms / level_alignments * 100:.2f}%")
    print(f"{level} merges: \t\t\t{level_merges}")
    print(f"{level} merges/alignements: \t{level_merges / level_alignments * 100:.2f}%")
    print("-" * 50)


# print(df_n2ms)
print(f"Total alignments: \t\t{all_alignments}")
print(f"Total n2m alignments: \t\t{all_n2ms}")
print(f"Total percentage of n2m: \t{all_n2ms / all_alignments * 100:.2f}%")
print(f"Total merges: \t\t\t{all_merges}")
print(f"Total merges/alignements: \t{all_merges / all_alignments * 100:.2f}%")
print("-" * 50) 
print(f"sent merges / total n2m: \t{all_sent_merges / all_n2ms * 100:.2f}%")
print(f"sent merges / total alignments: {all_sent_merges / all_alignments * 100:.2f}%")
print("-" * 50)

import os
import csv
import pandas as pd

levels = ["para", "sent"]

all_alignments = 0
all_n2ms = 0
all_merges = 0
all_sent_merges = 0

for level in levels:
    inputdir = f"aligned_sentences_{level}"
    outputdir = f"n2m_only/{level}_sents"
    os.makedirs(outputdir, exist_ok=True)

    level_alignments = 0
    level_n2ms = 0
    level_merges = 0

    all_langs_file = f"n2m_only/{level}_sents/all_langs_{level}.csv"
    with open(all_langs_file, 'w') as outf:
        writerA = csv.writer(outf)
        writerA.writerow(["langs", "system", "n2m", "source", "target", "n2mS", "n2mT"])
        # Extract language pairs and system
        for file in os.listdir(inputdir):
            filepath = os.path.join(inputdir, file)
            filename = os.path.basename(file)
            langs, _, system, _ = filename.split(".")
            
            count_n2ms = 0

            with open(filepath, 'r') as inf, open(os.path.join(outputdir, filename), 'w') as outf:
                reader = csv.reader(inf)
                next(reader)  # Skip header
                writer = csv.writer(outf)
                writer.writerow(["id", "source", "target", "n2m"])

                for row in reader:
                    level_alignments += 1
                    all_alignments += 1
                    n2m = row[3]
                    n2ms = n2m.split("-")[0]
                    n2mt = n2m.split("-")[1]
                    if n2m.split("-")[0] != n2m.split("-")[1]:
                        count_n2ms += 1
                        level_n2ms += 1
                        all_n2ms += 1
                        writer.writerow(row)
                        writerA.writerow([langs, system, n2m, row[1], row[2], n2ms, n2mt])
                    if n2ms > n2mt:
                        level_merges += 1
                        all_merges += 1


    if level == "sent":
        all_sent_merges = level_merges
    print(f"{level} alignments: \t\t{level_alignments}")
    print(f"{level} n2m alignments: \t\t{level_n2ms}")
    print(f"{level} percentage of n2m: \t{level_n2ms / level_alignments * 100:.2f}%")
    print(f"{level} merges: \t\t\t{level_merges}")
    print(f"{level} merges/alignements: \t{level_merges / level_alignments * 100:.2f}%")
    print("-" * 50)


# print(df_n2ms)
print(f"Total alignments: \t\t{all_alignments}")
print(f"Total n2m alignments: \t\t{all_n2ms}")
print(f"Total percentage of n2m: \t{all_n2ms / all_alignments * 100:.2f}%")
print(f"Total merges: \t\t\t{all_merges}")
print(f"Total merges/alignements: \t{all_merges / all_alignments * 100:.2f}%")
print("-" * 50) 
print(f"sent merges / total n2m: \t{all_sent_merges / all_n2ms * 100:.2f}%")
print(f"sent merges / total alignments: {all_sent_merges / all_alignments * 100:.2f}%")
print("-" * 50)

