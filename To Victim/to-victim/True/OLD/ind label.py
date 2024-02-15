import os
import pandas as pd
from tqdm import tqdm

# Get the current working directory
directory = os.getcwd()

# Define chunk size based on your system's memory capacity
chunk_size = 400000

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        input_file = os.path.join(directory, filename)
        output_file = os.path.join(directory, 'labeled_' + filename)

        # Get the total number of rows in the CSV file
        total_rows = sum(1 for _ in open(input_file, 'r'))

        # Initialize an empty DataFrame to store the result
        result_df = pd.DataFrame()

        # Create a tqdm progress bar
        with tqdm(total=total_rows, desc=f"Processing {filename}") as pbar:
            # Read the CSV file in chunks
            for chunk in pd.read_csv(input_file, chunksize=chunk_size):
                # Add a new column named 'label' with a default value of 1
                chunk['label'] = 1
                
                # Replace 'N/A' values with 0 in the current chunk
                chunk = chunk.fillna(0)
                
                # Concatenate the current chunk to the result DataFrame
                result_df = pd.concat([result_df, chunk], ignore_index=True)
                
                # Update the progress bar
                pbar.update(len(chunk))

        # Save the modified DataFrame back to a new CSV file
        result_df.to_csv(output_file, index=False)

        print(f"Processed {filename}. Output saved to {output_file}")
