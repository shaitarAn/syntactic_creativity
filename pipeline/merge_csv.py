import pandas as pd
import argparse

"""
Merge the DataFrames on the 'lang' and 'system' columns.
"""

parser = argparse.ArgumentParser()
parser.add_argument("--level", "-l", type=str)
args = parser.parse_args()

level = args.level

file_path1 = f'../results/{level}_alignment_scores.csv'
file_path2 = f'../results/{level}_n2m_scores.csv'

output_file_path = f'../results/{level}_syntax_scores.csv'

df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

merged_df = pd.merge(df1, df2, on=['lang', 'system'], how='outer')
merged_df['system'] = merged_df['system'].replace('llama', 'llama2')

merged_df.to_csv(output_file_path, index=False)

print("Merged file saved to", output_file_path)
