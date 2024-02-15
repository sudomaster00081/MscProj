import os
import pandas as pd

def combine_csv_files():
    # Get the current directory
    current_directory = os.getcwd()

    # List all files in the current directory
    files = os.listdir(current_directory)

    # Filter out only CSV files
    csv_files = [file for file in files if file.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the current directory.")
        return

    # Read the first CSV file to get the column names
    first_file = csv_files[0]
    df_combined = pd.read_csv(first_file)

    # Combine all CSV files
    for file in csv_files[1:]:
        df = pd.read_csv(file)
        df_combined = pd.concat([df_combined, df], ignore_index=True)

    # Write the combined dataframe to a new CSV file
    combined_filename = "combined.csv"
    df_combined.to_csv(combined_filename, index=False)

    print(f"All CSV files combined into '{combined_filename}'.")

if __name__ == "__main__":
    combine_csv_files()
