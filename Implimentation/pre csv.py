import pandas as pd

# Replace 'path_to_your_file' with the actual path to your CSV file
file_path = 'labeled_ddostrace.to-victim.20070804.csv'

# Read the CSV file, skipping the first row
df = pd.read_csv(file_path, skiprows=1)

# Convert each column to numeric
df = df.apply(pd.to_numeric, errors='coerce')

# Print each column name and its data type
for column in df.columns:
    print(f"{column}: {df[column].dtype}")
