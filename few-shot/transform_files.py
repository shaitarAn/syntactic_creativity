import csv
import os
import shutil

indir = "translated/para-level"
outdir = "inputs/paras"
for subdir in os.listdir(indir):
    prompttype = subdir
    print(prompttype)
    for file in os.listdir(os.path.join(indir, subdir)):
        if subdir == "ashuman":
            if "gpt4" in file:
                outfilename = file.replace("gpt4", "gpt4hum")
            else:
                outfilename = file.replace("gpt3", "gpt3hum")
        else:
            if "gpt4" in file:
                outfilename = file.replace("gpt4", "gpt4mch")
            else:
                outfilename = file.replace("gpt3", "gpt3mch")  

        # Construct full paths for input and output files
        input_path = os.path.join(indir, subdir, file)
        output_path = os.path.join(outdir, outfilename)

        # Copy the file to the output directory with the updated filename
        shutil.copy(input_path, output_path)


