import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'ddostrace.to-victim.20070804.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Add a new column 'label' with numeric values (e.g., 0)
df['label'] = 1

# Save the modified DataFrame back to the CSV file
df.to_csv('modified_ddostrace.to-victim.20070804.csv', index=False)
