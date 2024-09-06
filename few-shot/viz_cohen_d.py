import pandas as pd
import matplotlib.pyplot as plt

# Sample data file paths (replace these with your actual file paths)
data1 = "results/cohen_d_effect_size_humch.csv"
data2 = "../results/cohen_d_effect_size.csv"

# Load data files into pandas dataframes
df1 = pd.read_csv(data1)
df2 = pd.read_csv(data2)

# Filter rows where "System" value contains "gpt4"
df1 = df1[df1['System'].str.contains('gpt4')]
df2 = df2[df2['System'].str.contains('gpt4')]

# Concatenate the two dataframes
results_df = pd.concat([df1, df2], ignore_index=True)

# Filter out language names containing "news"
results_df = results_df[~results_df['Language'].str.contains('news')]

# Plot the effect size results
unique_languages = results_df['Language'].unique()
num_languages = len(unique_languages)

# Determine the number of rows and columns for subplots based on number of unique languages
num_cols = 5  # Fixed number of columns (adjust based on your preference)
num_rows = (num_languages + num_cols - 1) // num_cols  # Calculate number of rows needed

plt.figure(figsize=(16, 8))  # Adjust figsize based on the number of rows

colors = {'Paragraph': 'lightblue', 'Sentence': 'gray'}

# Iterate over each unique language
for idx, (lang, group) in enumerate(results_df.groupby('Language')):
    plt.subplot(num_rows, num_cols, idx + 1)  # Use dynamic subplot layout
    
    # Filter data for the current language
    lang_df = group
    
    # Get unique systems in the current language group
    unique_systems = lang_df['System'].unique()
    
    # Define positions for bars
    positions = range(len(unique_systems))
    width = 0.4  # Width of each bar
    
    # Plot bars for 'Paragraph' level
    paragraph_data = lang_df[lang_df['Level'] == 'Paragraph']
    plt.bar([p - width/2 for p in positions], paragraph_data['Cohen_d'], width=width, color='lightblue', label='Paragraph', alpha=0.8)
    
    # Plot bars for 'Sentence' level
    sentence_data = lang_df[lang_df['Level'] == 'Sentence']
    plt.bar([p + width/2 for p in positions], sentence_data['Cohen_d'], width=width, color='gray', label='Sentence', alpha=0.8)
    
    plt.title(f"{lang}")
    plt.xticks(positions, unique_systems, rotation=45)
    # remove borders
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    # add a black line at y=0
    plt.axhline(0, color='black', linewidth=0.5)
    # make grid lines more visible
    plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
# add legend outside of the plot
plt.legend(loc='lower right', bbox_to_anchor=(3, -0.1), ncol=2)
plt.show()
plt.close()

# Sample data file paths (replace these with your actual file paths)
data1 = "results/cohen_d_effect_size_humch.csv"
data2 = "../results/cohen_d_effect_size.csv"

# Load data files into pandas dataframes
df1 = pd.read_csv(data1)
df2 = pd.read_csv(data2)

# Concatenate the two dataframes
results_df = pd.concat([df1, df2], ignore_index=True)

# Filter out language names containing "news"
results_df = results_df[~results_df['Language'].str.contains('news')]
results_df = results_df[~results_df['System'].str.contains('llama')]

# Calculate the average effect size for each system and level
avg_effect_size = results_df.groupby(['System', 'Level'])['Cohen_d'].mean().unstack()

# Rename 'gpt4' to 'zero-shot'
avg_effect_size = avg_effect_size.rename(index={'gpt4': 'gpt4-None-0'})
avg_effect_size = avg_effect_size.rename(index={'gpt4hum': 'gpt4-human-5'})
avg_effect_size = avg_effect_size.rename(index={'gpt4mch': 'gpt4-machine-5'})
avg_effect_size = avg_effect_size.rename(index={'gpt3hum': 'gpt3-human-5'})
avg_effect_size = avg_effect_size.rename(index={'gpt3mch': 'gpt3-machine-5'})
avg_effect_size = avg_effect_size.rename(index={'gpt3': 'gpt3-deprecated-5'})
print(avg_effect_size)

# Plot the average effect size
# plt.figure(figsize=(10, 8))
ax = avg_effect_size.plot(kind='bar', stacked=False, colormap='RdYlGn', figsize=(10, 8))
# rotate x-axis labels to 45 degrees
plt.xticks(rotation=25)
plt.xlabel('')
plt.ylabel('Average Cohen\'s d')
plt.title('Average Cohen\'s d across languages')
# place legend in the bottom center
plt.legend(loc='lower right', bbox_to_anchor=(1, 0.0), ncol=1)
# draw a line at y=-0.244745
plt.axhline(y=-0.244745, color='black', linewidth=0.5)
# save the plot as a PNG file
plt.savefig('avg_effect_size.png', bbox_inches='tight')
plt.show()
plt.close()
