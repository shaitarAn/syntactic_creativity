import os
import pandas as pd

def count_detected_translations(input_dir):
    # Initialize an empty DataFrame to store the aggregated counts
    result_df = pd.DataFrame(columns=['langs', 'prompt', 'MISS'])

    # Iterate over each file in the specified directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_dir, filename)

            # Extract the language and prompt name from the filename
            filename_parts = filename.split('.')
            if len(filename_parts) < 4:
                continue  # Skip files that don't match expected naming convention
            
            langs = filename_parts[0]  # Extract languages
            promptname = filename_parts[2]  # Extract promptname

            # Load the CSV file into a DataFrame
            try:
                df = pd.read_csv(filepath)
            except pd.errors.EmptyDataError:
                continue  # Skip empty files or files that cannot be read

            # Count occurrences of "DETECTED" in the 'translation' column
            count_deleted = df['translation'].str.contains('DETECTED').sum()

            # Append results to the result DataFrame
            result_df = result_df.append({'langs': langs, 'prompt': promptname, 'MISS': count_deleted},ignore_index=True)

    return result_df

def main():
    input_dir = 'test_outputs'  # Specify the directory containing CSV files
    output_file = 'detected_translations_summary.csv'  # Output CSV filename

    # Count "DETECTED" translations
    result_df = count_detected_translations(input_dir)

    # Save the result DataFrame to a CSV file
    result_df.to_csv(output_file, index=False)
    print(f"Result saved to {output_file}")

if __name__ == "__main__":
    main()
