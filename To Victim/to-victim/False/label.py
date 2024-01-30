import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'ddostrace.to-victim.20070804.csv'  # Replace with the actual path to your CSV file

# Specify the data types for the problematic columns
column_types = {'frame.len': pd.Int64Dtype(),
                'frame.time_delta_displayed': pd.Int64Dtype(),
                'tcp.dstport': pd.Int64Dtype(),
                'udp.dstport': pd.Int64Dtype(),
                'ip.proto': pd.Int64Dtype(),
                'frame.time_relative': pd.Int64Dtype()}

# Read the CSV file with specified data types and skip the first row
df = pd.read_csv(file_path, dtype=column_types, low_memory=False, skiprows=1)

# Print unique values in the problematic columns
problematic_columns = ['frame.time_delta_displayed', 'tcp.dstport', 'udp.dstport']
for col in problematic_columns:
    # Remove leading and trailing whitespaces from column names
    col = col.strip()
    try:
        unique_values = df[col].unique()
        print(f"Unique values in {col}: {unique_values}")
    except KeyError:
        print(f"Column {col} not found in the DataFrame.")

# Handle problematic values
df[problematic_columns] = df[problematic_columns].apply(pd.to_numeric, errors='coerce')

# Convert the columns to integer type
df[problematic_columns] = df[problematic_columns].astype(pd.Int64Dtype(), errors='ignore')

# Add a new column 'label' with numeric values (e.g., 0)
df['label'] = 0

# Save the modified DataFrame back to the CSV file
df.to_csv('modified_ddostrace.csv', index=False)
