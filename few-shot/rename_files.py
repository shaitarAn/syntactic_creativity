import os, sys

persona = sys.argv[1]

def rename_files_with_suffix(directory):
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        # Split the filename into base name and extension
        # base_name, extension = os.path.splitext(filename)
        # system = file.split(".")[-3]
        if "gpt3." in filename:
            new_filename = filename.replace("gpt3.", f"gpt3{persona}.")
        else:
            new_filename = filename.replace("gpt4.", f"gpt4{persona}.")
        
        # # Check if the filename has an extension
        # if extension:
        #     # if "human" in base_name:
        #         # continue
        #     # Construct the new filename with "1" inserted before the extension
        #     new_filename = f"{base_name}.1{extension}"
            
        # Create the full path for the old and new filenames
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} -> {new_path}")

# Specify the directory containing the files
directory = "inputs/paras"

# Call the function to rename files in the specified directory
rename_files_with_suffix(directory)
