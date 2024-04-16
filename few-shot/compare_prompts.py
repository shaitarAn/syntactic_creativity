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
    output_file = 'detected_translations_summary_problem_langs.csv'  # Output CSV filename

    # Count the number of "DETECTED" translations in each CSV file
    count_detected_translations_df = count_detected_translations(input_dir)

    # Save the aggregated counts to a CSV file
    count_detected_translations_df.to_csv(output_file, index=False)

    # visualize the result with a bar plot in a blue gradient
    count_detected_translations_df.plot(kind='bar', x='langs', stacked=False, colormap='RdYlGn', figsize=(10, 6))

    # move the legend to the upper left corner
    plt.legend(loc='lower right', fancybox=True, shadow=True, ncol=1, title='Prompt types')
    # add a title
    plt.title('Ability of Llama to produce target language. Yes quantization.')
    # remove the x-axis label
    plt.xlabel('')
    # add a y-axis label
    plt.ylabel('Number of detected translations')
    # save the plot as a PNG file
    plt.savefig('detected_translations_llama_nq.png', bbox_inches='tight')
    
    plt.show()

    # calculate the average of the inst1 and other columns
    avg_inst1 = count_detected_translations_df['inst1'].mean()
    avg_karp1 = count_detected_translations_df['karp1'].mean()
    avg_hum1 = count_detected_translations_df['hum1'].mean()
    avg_mach1 = count_detected_translations_df['mach1'].mean()
    avg_html1 = count_detected_translations_df['html1'].mean()
    avg_inst5 = count_detected_translations_df['inst5'].mean()
    avg_karp5 = count_detected_translations_df['karp5'].mean()

    # create a new DataFrame with the averages
    avg_df = pd.DataFrame({'inst1': avg_inst1, 'inst5': avg_inst5, 'karp1': avg_karp1, 'karp5': avg_karp5, 'hum1': avg_hum1, 'mach1': avg_mach1, 'html1': avg_html1}, index=[0])

    # visualize the average with a bar plot in a blue gradient
    ax = avg_df.plot(kind='bar', stacked=False, colormap='RdYlGn', figsize=(10, 6))

    # draw a black border around the bars
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
    
    # Annotate each bar with its value
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 10), 
                    textcoords='offset points')
    
    # Add a title and labels
    # plt.title('Average number of detected translations')
    plt.xlabel('Prompt types')
    plt.ylabel('Average number of detected translations')

    # add black line around the bars
    plt.gca().spines['top'].set_color('black')

    # display the bars starting at 6 on the y-axis
    plt.ylim(8, 10)

    # save the plot as a PNG file
    plt.savefig('avg_detected_translations_nq.png', bbox_inches='tight')

    # Display the plot
    plt.show()

if __name__ == "__main__":
    main()


# iterate over each file in the specified directory
