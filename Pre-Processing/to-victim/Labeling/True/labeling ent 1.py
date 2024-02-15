import pandas as pd

# Read the CSV file
filename = "combined True.csv"  # Replace "your_csv_file.csv" with the actual filename
df = pd.read_csv(filename)

# Add a column named "label" with integer value 0
df['label'] = 1

# Save the modified DataFrame to a new CSV file
new_filename = "labeled_" + filename
df.to_csv(new_filename, index=False)

print("DataFrame with 'label' column added successfully saved as:", new_filename)
