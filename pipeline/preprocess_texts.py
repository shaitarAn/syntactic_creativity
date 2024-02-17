import os
from utils import normalize_punct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--level", "-l", type=str)
parser.add_argument("--workdir", "-wd", type=str)
args = parser.parse_args()

level = args.level
workdir = args.workdir

outputdir = f"{workdir}/{level}s_cleaned"

def remove_ja_chars(line):
    line = line.replace("」", "")
    line = line.replace("「", "")
    line = line.replace("。。。。。。", "。。。")
    return line

for f in os.listdir(f"{workdir}/{level}s"):
    f = os.path.join(f"{workdir}/{level}s", f)
    filename = os.path.basename(f)
    # Remove "_lit" from the filename
    filename = filename.replace("_lit", "")
    filename = filename.replace("gtr", "nmt")
    filename = filename.replace("deepl", "nmt")
    outfile = os.path.join(outputdir, filename)
    with open(f, "r") as inf, open(outfile, "w") as outf:
        for line in inf.readlines():
            line = normalize_punct(line)
            line = remove_ja_chars(line)
            outf.write(line.strip() + "\n")