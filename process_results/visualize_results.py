import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create a DataFrame
# data = {
#     'system': ['gpt3', 'gpt4', 'human', 'llama'],
#     'xwr': [1.0495, 1.032, 1.562, 1.1615],
#     'n2mR': [0.155067, 0.128926, 0.18448, 0.146191],
#     'length_var': [0.624328, 0.717716, 0.720074, 0.675851]
# }

data = "../results/para_syntax_scores.csv"
data = pd.read_csv(data)
df = pd.DataFrame(data)

# print(df)
# average xwr, n2mR, length_var scores per system
df = pd.DataFrame(data, columns=['system', 'xwr', 'n2mR', 'length_var'])
df = df.groupby(['system']).mean().reset_index()

# Reshape the DataFrame for seaborn
df_melted = df.melt(id_vars='system', var_name='Metric', value_name='Score')

# Create the plot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

palette = sns.color_palette("muted", n_colors=4)
sns.barplot(x='Metric', y='Score', hue='system', data=df_melted, palette=palette)

plt.title('Average Scores per System by Metric for Paragraph-level Translations')
plt.ylabel('Average Score')
plt.xlabel('Metric')

plt.tight_layout()
plt.show()
plt.close()

# create a plot per language

dfl = pd.DataFrame(data, columns=['lang', 'system', 'xwr', 'n2mR', 'length_var'])
dfl = dfl.groupby(['lang', 'system']).mean().reset_index()

# Reshape the DataFrame for seaborn
df_meltedl = dfl.melt(id_vars=['lang', 'system'], var_name='Metric', value_name='Score')

# Create the plot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

palette = sns.color_palette("muted", n_colors=4)
sns.barplot(x='Metric', y='Score', hue='system', data=df_meltedl, palette=palette)

plt.title('Average Scores per System by Metric for Paragraph-level Translations')
plt.ylabel('Average Score')
plt.xlabel('Metric')

plt.tight_layout()
plt.show()
plt.close()

# create a plot per language


