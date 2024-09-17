import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.multitest import multipletests

level = 'Sentence'

# Load data
data = pd.read_csv("../few-shot/results/combined_results.csv")

# replace system name nmt to Goog;e
data['System'] = data['System'].replace('nmt', 'Google')

# select only level of interest
data = data[data['Level'] == level]
# select only rows where p-value is less than 0.05
# data = data[data['p_value'] < 0.05]

# Correcting for multiple comparisons using Benjamini/Hochberg method
_, corrected_p_values, _, _ = multipletests(data['p_value'], method='fdr_bh', alpha=0.05)
data['corrected_p_value'] = corrected_p_values

# Filter to only significant results after correction
significant_data = data[data['corrected_p_value'] < 0.05]

# print the significant_data
print(significant_data)
# print as a ;latex table
print(significant_data.to_latex(index=False))



# make subplot for each language, group by system, fill bars by level
plt.figure(figsize=(16, 5))
sns.barplot(x='Language', y='Cohen_d', hue='System', data=significant_data)
plt.title(f'Cohen\'s d for {level}-Level Translations')
plt.xlabel('')
plt.ylabel('Cohen\'s d')
plt.legend(title='System', loc='best')
# add a horizontal line at 0.2 and -0.2
plt.axhline(y=0.2, color='r', linestyle='--', linewidth=1)
plt.axhline(y=-0.2, color='r', linestyle='--', linewidth=1)
# add a horizontal line at 0
plt.axhline(y=0, color='black', linewidth=1)
# remove horizontal grid lines
plt.grid(axis='x')
# increase the font size
plt.xticks(fontsize=18, rotation=45, ha='right')
plt.yticks(fontsize=18)
plt.legend(fontsize=20)

plt.tight_layout()
# save the plot
plt.savefig(f'../viz/few-shot_cohen_{level}.png')
plt.show()