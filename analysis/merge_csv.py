import pandas as pd
import argparse

"""
Merge the DataFrames on the 'lang' and 'system' columns.
"""

parser = argparse.ArgumentParser()
parser.add_argument("--level", "-l", type=str)
parser.add_argument("--output_dir", "-o", type=str)
args = parser.parse_args()

level = args.level

file_path1 = f'{args.output_dir}/results/{level}_alignment_scores.csv'
file_path2 = f'{args.output_dir}/results/{level}_n2m_scores.csv'

output_file_path = f'{args.output_dir}/results/{level}_syntax_scores.csv'

df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

merged_df = pd.merge(df1, df2, on=['lang', 'system', 'file'], how='inner')
# merged_df['system'] = merged_df['system'].replace('llama', 'llama2')

merged_df.to_csv(output_file_path, index=False)

print("Merged file saved to", output_file_path)
