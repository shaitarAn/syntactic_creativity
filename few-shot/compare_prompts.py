import os
import pandas as pd
import matplotlib.pyplot as plt

def count_detected_translations(input_dir):
    # Initialize an empty DataFrame to store the aggregated counts
    result_df = pd.DataFrame(columns=['langs', 'inst1', 'inst5', 'karp1', 'karp5', 'hum1', 'mach1', 'html1'])

    # Iterate over each file in the specified directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_dir, filename)

            # Extract the language and prompt name from the filename
            filename_parts = filename.split('.')
            if len(filename_parts) < 4:
                continue  # Skip files that don't match expected naming convention
            
            langs = filename_parts[0]  # Extract languages
            promptname = filename_parts[3]  # Extract promptname

            # Load the CSV file into a DataFrame
            try:
                df = pd.read_csv(filepath)
            except pd.errors.EmptyDataError:
                continue  # Skip empty files or files that cannot be read

            # Count the number of "DETECTED" translations
            count = df['translation'].str.contains('DETECTED').sum()

            # add the count to the result DataFrame
            if langs not in result_df['langs'].values:
                result_df = result_df.append({'langs': langs}, ignore_index=True)
            result_df.loc[result_df['langs'] == langs, promptname] = 10 - count

    return result_df

def main():
    input_dir = 'test_outputs'  # Specify the directory containing CSV files
    output_file = 'detected_translations_summary.csv'  # Output CSV filename

    # Count the number of "DETECTED" translations in each CSV file
    count_detected_translations_df = count_detected_translations(input_dir)

    # Save the aggregated counts to a CSV file
    count_detected_translations_df.to_csv(output_file, index=False)

    # visualize the result with a bar plot in a blue gradient
    count_detected_translations_df.plot(kind='bar', x='langs', stacked=False, colormap='RdYlGn_r', figsize=(10, 6))

    plt.show()

if __name__ == "__main__":
    main()



