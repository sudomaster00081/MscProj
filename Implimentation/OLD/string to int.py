import pandas as pd
import os

# Process each .csv file in the current directory
for file_name in os.listdir('.'):
    if file_name.endswith('.csv'):
        file_path = os.path.join('.', file_name)
        
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # List of columns to convert to integer type
        columns_to_convert = ['frame.len', 'frame.time_delta_displayed', 'tcp.dstport', 'udp.dstport', 'ip.proto', 'frame.time_relative']

        # Print columns with non-numeric values before conversion
        non_numeric_columns = df[columns_to_convert].applymap(lambda x: not str(x).replace('.', '').isdigit())
        columns_with_issue = non_numeric_columns.any()
        problematic_columns = columns_with_issue[columns_with_issue].index.tolist()
        print(f"Columns with non-numeric values in {file_name}: {problematic_columns}")

        # Print unique values in the problematic columns
        for col in problematic_columns:
            unique_values = df[col].unique()
            print(f"Unique values in {col}: {unique_values}")

        # Replace or drop non-finite values before converting to integers
        df[columns_to_convert] = df[columns_to_convert].replace(['inf', '-inf'], pd.NA)  # Replace inf with pd.NA

        # Replace problematic values with NaN before converting
        for col in columns_to_convert:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convert the columns to integer type
        df[columns_to_convert] = df[columns_to_convert].astype(pd.Int64Dtype(), errors='ignore')

        # Save the modified DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

        print(f"Conversion complete for {file_name}\n")
