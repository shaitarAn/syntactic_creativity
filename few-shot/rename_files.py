import os

def rename_files_with_suffix(directory):
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        # Split the filename into base name and extension
        base_name, extension = os.path.splitext(filename)
        
        # Check if the filename has an extension
        if extension:
            # Construct the new filename with "1" inserted before the extension
            new_filename = f"{base_name}.1{extension}"
            
            # Create the full path for the old and new filenames
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")

# Specify the directory containing the files
directory = "test_outputs_q_all_langs"

# Call the function to rename files in the specified directory
rename_files_with_suffix(directory)
