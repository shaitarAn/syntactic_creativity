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

level = "para"

data = f"../few-shot/results/{level}_syntax_scores.csv"
data = pd.read_csv(data)
df = pd.DataFrame(data)

# print(df)

# Filter out rows where system == 'xxx'
df = df[df['system'] != 'gpt4mch']
df = df[df['lang'] != 'de-en_news']
df = df[df['lang'] != 'en-de_news']

# Average xwr, n2mR, length_var scores per system
df = pd.DataFrame(df, columns=['system', 'xwr_mean', 'n2mR', 'length_var'])
df = df.groupby(['system']).mean().reset_index()

print(df)

# Reshape the DataFrame for seaborn
df_melted = df.melt(id_vars='system', var_name='Metric', value_name='Score')

# Create the plot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

palette = sns.color_palette("muted", n_colors=3)
sns.barplot(x='Metric', y='Score', hue='system', data=df_melted, palette=palette)

plt.title('')
plt.ylabel('Average Score')
plt.xlabel('Metric')

plt.tight_layout()
# Save the plot instead of displaying it
plt.savefig(f"{level}_scores_plot.png", bbox_inches="tight")

# Optional: If you're on a server, remove plt.show() to avoid the display error
plt.close()

# create a plot per language
df = pd.DataFrame(data)
# Filter out rows where system == 'xxx'
df = df[df['system'] != 'gpt4mch']
df = df[df['lang'] != 'de-en_news']
df = df[df['lang'] != 'en-de_news']

# Average xwr, n2mR, length_var scores per system
df = pd.DataFrame(df, columns=['lang', 'system', 'xwr_mean', 'n2mR', 'length_var'])
dfl = df.groupby(['lang', 'system']).mean().reset_index()

# Reshape the DataFrame for seaborn
df_meltedl = dfl.melt(id_vars=['lang', 'system'], var_name='Metric', value_name='Score')

# Create the plot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

palette = sns.color_palette("muted", n_colors=3)
sns.barplot(x='Metric', y='Score', hue='system', data=df_meltedl, palette=palette)

plt.title('Average Scores per System by Metric for Paragraph-level Translations')
plt.ylabel('Average Score')
plt.xlabel('Metric')

plt.tight_layout()
plt.savefig(f"{level}_per_lang.png", bbox_inches="tight")
plt.close()


