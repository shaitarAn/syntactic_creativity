import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
csv_file = "../analysis/xwr_par3_en-de.csv"
print(csv_file)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)
df.dropna()

# Plot boxplots for each column in the DataFrame
plt.figure(figsize=(10, 6))  # Set the figure size (width, height)

# Customize boxplot appearance
boxprops = dict(linewidth=2, color='blue')  # Customize box properties
medianprops = dict(linewidth=2, color='red')  # Customize median properties

# Create boxplot
df.boxplot(column=df.columns.tolist(),  # Plot all columns
           boxprops=boxprops,  # Customize box properties
           medianprops=medianprops)  # Customize median properties

# Set plot labels and title
plt.xlabel('Methods')  # X-axis label
plt.ylabel('Performance')  # Y-axis label
plt.title('Performance Comparison')  # Plot title

# Show plot
plt.show()
plt.close()
