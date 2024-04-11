import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
csv_file = "../analysis/par3_de_xwr.csv"
print(csv_file)

# group by the column "book" and plot columns GT,human1,human2,human3 if human3 is present
df = pd.read_csv(csv_file)

df_grouped = df.groupby("book")

# for each book create a boxplot of the columns GT,human1,human2 and human3 if present
for name, group in df_grouped:
    print(name)
    print(group)
    group.boxplot(column=["GT", "human1", "human2", "human3"])
    plt.title(name)
    plt.show()

    

