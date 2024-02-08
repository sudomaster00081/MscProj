import pandas as pd

# Replace 'ddostrace.to-victim.20070804.csv' with your input file name
input_file = 'ddostrace.to-victim.20070804.csv'
output_file = 'labeled_' + input_file

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Add a new column named 'label' with a default value of 0
df['label'] = 0

# Replace 'N/A' values with 0 in the entire DataFrame
df = df.fillna(0)

# Save the modified DataFrame back to a new CSV file or overwrite the existing file
df.to_csv(output_file, index=False)

print(f"Script executed successfully. Output saved to {output_file}")
