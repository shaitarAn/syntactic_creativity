import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load data
df = pd.read_csv('../few-shot/results/cohen_d_effect_size.csv')

# Define color schemes for different languages with pastel colors
shared_colors = {
    'en': (0.4, 0.6, 1),   # Light blue
    'ja': (0.9, 0.3, 0.5), # Dark red
    'de': (0.7, 0.9, 0.75), # Lighter green
    'pl': (0.8, 0.75, 0.7)  # Light yellow
}

# Define color schemes for source languages
source_lang_color_schemes = {
    **shared_colors,
    'ru': (0.6, 0.3, 0.8),  # Lighter purple
    'cs': (0.1, 0.7, 0.8),  # Lighter cyan
    'fr': (0.9, 0.5, 0.4), # Light orange
    'zh': (0.6, 0.8, 0.9)   # Lighter teal
}

target_lang_color_schemes = shared_colors

# Define thresholds
thresholds = [-float('inf'), -0.5, -0.2, 0.2, 0.5, float('inf')]
labels = ['large -', 'mid -', 'small', 'mid +', 'large +']

# Create subsets based on thresholds
groups = pd.cut(df['Cohen_d'], bins=thresholds, labels=labels)

# Create subsets based on thresholds
df['Cohen_d_group'] = pd.cut(df['Cohen_d'], bins=thresholds, labels=labels)

# Extract target language and merge en and en_news, and replace 'de_news' with 'de'
df['Target_Lang'] = df['Language'].str.split('-').apply(lambda x: 'en' if x[1] in ['en', 'en_news'] else 'de' if x[1] == 'de_news' else x[1])

# extract source language
df['Source_Lang'] = df['Language'].str.split('-').apply(lambda x: x[0])

# ############################ System Distribution ############################

# Calculate percentage of occurrences for System within each group
system_percentages = df.groupby([groups, 'System']).size().unstack().apply(lambda x: x / x.sum(), axis=1)

# Plot System percentages
ax = system_percentages.plot(kind='bar', stacked=True, colormap='RdYlGn_r')  # Set colormap to Set3
plt.title('Percentage of System in each Cohen_d group')
plt.xlabel('Effect Size')
plt.ylabel('Percentage')
plt.legend(title='System')
plt.xticks(rotation=45)

# Save as a PDF
plt.savefig('../viz/few-shot_cohen_sys_distribution.pdf')

# Show plot
plt.show()
plt.close()

# ############################ System Distribution for Japanese ############################

# df['Cohen_d_group'] = pd.cut(df['Cohen_d'], bins=thresholds, labels=labels)

# Filter DataFrame for Japanese language
ja_df = df[df['Target_Lang'] == 'ja']

# Create subsets based on thresholds for Japanese language
ja_df['Cohen_d_group'] = pd.cut(ja_df['Cohen_d'], bins=thresholds, labels=labels)

# Calculate percentage of occurrences for System within each group for Japanese language
ja_system_percentages = ja_df.groupby(['Cohen_d_group', 'System']).size().unstack().apply(lambda x: x / x.sum(), axis=1)

# Plot System percentages for Japanese language
ax = ja_system_percentages.plot(kind='bar', stacked=True, colormap='Blues')  # Set colormap to RdYlGn_r
plt.title('Percentage of System in each Cohen_d group for Japanese Language')
plt.xlabel('Effect Size')
plt.ylabel('Percentage')
plt.legend(title='System')
plt.xticks(rotation=45)

# Save as a PDF
plt.savefig('../viz/few-shot_cohen_sys_distribution_japanese.pdf')

# Show plot
plt.show()
plt.close()


# ############################ Level Distribution ############################

# Calculate percentage of occurrences for Level within each group
level_percentages = df.groupby([groups, 'Level']).size().unstack().apply(lambda x: x / x.sum(), axis=1)

# Plot Level percentages
level_percentages.plot(kind='bar', stacked=True)
plt.title('Percentage of Level in each Cohen_d group')
plt.xlabel('Effect Size')
plt.ylabel('Percentage')
plt.legend(title='Level')
plt.xticks(rotation=45)
# save as a pdf
plt.savefig('../viz/few-shot_cohen_level_distribution.pdf')
# plt.show()
plt.close()

# ############################ Language Distribution ############################

# Calculate percentage of occurrences for Language within each group
language_percentages = df.groupby([groups, 'Language']).size().unstack().apply(lambda x: x / x.sum(), axis=1)

# Plot Language percentages
language_percentages.plot(kind='bar', stacked=True, figsize=(7.75, 5.5), colormap='tab20')
plt.title('Percentage of Language in each Cohen_d group')
plt.xlabel('Effect Size')
plt.ylabel('Percentage')
plt.legend(title='Language')
# anchor the legend
plt.legend(loc='center', bbox_to_anchor=(1.15, 0.5))
plt.xticks(rotation=45)
plt.tight_layout()
# save as a pdf
plt.savefig('../viz/few-shot_cohen_language_distribution.pdf')
# save as a png
plt.savefig('../viz/few-shot_cohen_language_distribution.png')
# plt.show()
plt.close()

# ############################ Source-Target Language Distributions ############################

# Plot Language percentages
plt.figure(figsize=(5, 4))
for lang, color in target_lang_color_schemes.items():
    lang_df = df[df['Target_Lang'] == lang]
    lang_df['Cohen_d_group'].value_counts().sort_index().plot(kind='bar', color=color, label=lang)  

plt.title('Effect Size Distribution by Target Language')
plt.xlabel('Effect Size')
plt.ylabel('Count')
plt.legend(title='Target Language')
plt.xticks(rotation=45)
plt.tight_layout()
# save as a pdf
plt.savefig('../viz/few-shot_cohen_target_lang_distribution.pdf')
# plt.show()
plt.close()

# Plot Language percentages
plt.figure(figsize=(5, 5))
for lang, color in source_lang_color_schemes.items():
    lang_df = df[df['Source_Lang'] == lang]
    lang_df['Cohen_d_group'].value_counts().sort_index().plot(kind='bar', color=color, label=lang)

plt.title('Effect Size Distribution by Source Language')
plt.xlabel('Effect Size')
plt.ylabel('Count')
plt.legend(title='Source Language')
plt.xticks(rotation=45)
plt.tight_layout()
# save as a pdf
plt.savefig('../viz/few-shot_cohen_source_lang_distribution.pdf')
# plt.show()
plt.close()


# ############################ Source Language and Level Distribution ############################
# Initialize legend entries list
legend_entries = []

# Initialize subplots
fig, ax = plt.subplots(figsize=(10, 6))

# Define bar width
bar_width = 0.35

# Iterate over levels
for level_idx, level in enumerate(['Sentence', 'Paragraph']):
    # Initialize x position for bars
    x_pos = np.arange(len(labels)) + level_idx * bar_width

    # Initialize heights for stacked bars
    bottom = np.zeros(len(labels))

    # Iterate over source languages
    for lang, color in source_lang_color_schemes.items():
        # Create dataframe for the current language and level
        lang_df = df[(df['Source_Lang'] == lang) & (df['Level'] == level)]
        # Calculate counts for Cohen_d groups
        counts = lang_df['Cohen_d_group'].value_counts().sort_index()
        # Plot bars and stack them
        ax.bar(x_pos, counts, color=color, width=bar_width, bottom=bottom, alpha=0.7, edgecolor='black', label=lang if lang not in legend_entries else None, zorder=3)
        # Update bottom values for stacking
        bottom += counts

        # Add legend entry for the first language encountered
        if lang not in legend_entries:
            legend_entries.append(lang)

    # Add level labels under each group of bars
    for i, xpos in enumerate(x_pos):
        if level == 'Sentence':
            level_text = 'Sent'
        else:
            level_text = 'Para'
        # place the level text over each bar in each group
            
        ax.text(xpos + bar_width // 2, bottom[i] + 1, level_text, ha='center', va='top', fontsize=10, fontweight='bold')
            
# Set title and labels
plt.title('Effect Size Distribution by Source Language')
plt.xlabel("Cohen's d Effect Size")
plt.ylabel('Number of Documents')
plt.xticks(np.arange(len(labels)) + bar_width / 2, labels)
plt.legend(title='Source Language')
plt.grid(axis='y', zorder=0)  # Add grid
plt.tight_layout()

# Save figure
plt.savefig('../viz/few-shot_cohen_source_lang_level_distribution.pdf')
# save as a png
plt.savefig('../viz/few-shot_cohen_source_lang_level_distribution.png')
plt.show()
plt.close()

# ############################ Target Language and Level Distribution ############################
# Initialize legend entries list
legend_entries = []

# Initialize subplots
fig, ax = plt.subplots(figsize=(10, 6))

# Define bar width
bar_width = 0.35

# Iterate over levels
for level_idx, level in enumerate(['Sentence', 'Paragraph']):
    # Initialize x position for bars
    x_pos = np.arange(len(labels)) + level_idx * bar_width

    # Initialize heights for stacked bars
    bottom = np.zeros(len(labels))

    # Iterate over target languages
    for lang, color in target_lang_color_schemes.items():
        # Create dataframe for the current language and level
        lang_df = df[(df['Target_Lang'] == lang) & (df['Level'] == level)]
        # Calculate counts for Cohen_d groups
        counts = lang_df['Cohen_d_group'].value_counts().sort_index()
        # Plot bars and stack them
        ax.bar(x_pos, counts, color=color, width=bar_width, bottom=bottom, alpha=0.7, edgecolor='black', label=lang if lang not in legend_entries else None, zorder=3)
        # Update bottom values for stacking
        bottom += counts

        # Add legend entry for the first language encountered
        if lang not in legend_entries:
            legend_entries.append(lang)

    # Add level labels under each group of bars
    for i, xpos in enumerate(x_pos):
        if level == 'Sentence':
            level_text = 'Sent'
        else:
            level_text = 'Para'
        # Place the level text over each bar in each group
        ax.text(xpos + bar_width // 2, bottom[i] + 1, level_text, ha='center', va='top', fontsize=10, fontweight='bold')

# Set title and labels
plt.title('Effect Size Distribution by Target Language')
plt.xlabel("Cohen's d Effect Size")
plt.ylabel('Number of Documents')
plt.xticks(np.arange(len(labels)) + bar_width / 2, labels)
plt.legend(title='Target Language')
plt.grid(axis='y', zorder=0)  # Add grid
plt.tight_layout()

# Save figure
plt.savefig('../viz/few-shot_cohen_target_lang_level_distribution.pdf')
# save as a png
plt.savefig('../viz/few-shot_cohen_target_lang_level_distribution.png')
plt.show()
plt.close()
