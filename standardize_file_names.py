import os
import shutil
import re

""" iterate through all files in 2 directories and copy them to a new directory with standardized names """

# src_dir1 is a directory of directories
src_dir1 = "data/littrans/"

# src_dir2 is a directory of directories
src_dir2 = "data/wmt23/"

# create a new directory
dst_dir = "data/all/"
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

languages = re.compile(r"_([a-z]{2}-[a-z]{2})_(\w+).txt")

for book in os.listdir(src_dir1):
    # print(book)
    if os.path.isdir(os.path.join(src_dir1, book)):
        for file in os.listdir(os.path.join(src_dir1, book)):
            # print(file)
            # match language codes
            match = languages.search(file)
            if match:
                langs = match.group(1)
                langs = langs + "_lit"
                # print(langs)
                system = match.group(2)
                # print(system)
                # create new filename
                if system == "target":
                    new_filename = f"{langs}.human.txt"
                elif system == "para":
                    new_filename = f"{langs}.para3.txt"
                else:
                    new_filename = f"{langs}.{system}.txt"
                # copy file to new directory with new filename
                shutil.copy(os.path.join(src_dir1, book, file), os.path.join(dst_dir, new_filename))

for file in os.listdir(src_dir2):
    if file.endswith("txt"):
        name_parts = file.split(".")
        langs = name_parts[0]
        system = name_parts[1]
        if langs == "de-en":
            langs = "de-en_news"
        if system == "src":
            new_filename = f"{langs}.source.txt"
        else:
            new_filename = f"{langs}.human.txt"

        shutil.copy(os.path.join(src_dir2, file), os.path.join(dst_dir, new_filename))


