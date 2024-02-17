import pandas as pd

# Read the CSV file
dfs = pd.read_csv("comet_scores_sent.csv")

# Pivot the DataFrame
dfs_pivot = dfs.pivot(index='lang', columns='system', values='score').reset_index()

# Reorder the columns
desired_order = ['lang', 'gpt3', 'gpt4', 'llama', 'nmt']
dfs_reordered = dfs_pivot[desired_order]

# Display the rearranged DataFrame
print(dfs_reordered)

dfp = pd.read_csv("comet_scores_para.csv")

# Pivot the DataFrame
dfp_pivot = dfp.pivot(index='lang', columns='system', values='score').reset_index()

# Reorder the columns
desired_order = ['lang', 'gpt3', 'gpt4', 'llama']
dfp_reordered = dfp_pivot[desired_order]
# rename columns
dfp_reordered.columns = ['lang', 'gpt3_para', 'gpt4_para', 'llama2_para']

# join the two dataframes based on the language column
df = pd.merge(dfs_reordered, dfp_reordered, on='lang')

# Display the rearranged DataFrame
print(df)

# rearrange the columns
desired_order = ['lang', 'gpt3', 'gpt3_para', 'gpt4', 'gpt4_para', 'llama','llama2_para', 'nmt',]
df = df[desired_order]


# rmodify all values by multiplying them by 10 and then rounding to 2 decimal places
df.iloc[:, 1:] = df.iloc[:, 1:] * 10
df.iloc[:, 1:] = df.iloc[:, 1:].round(2)

# modify all values in the lang column that end with "_news", replace "_news" with "*"
df['lang'] = df['lang'].str.replace("_news", "*")
# Display the rearranged DataFrame
print(df)
# save to a latex table
df.to_latex("comet_scores.tex", index=False)
