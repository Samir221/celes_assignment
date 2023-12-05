import os
import pandas as pd


def view_data(folder_path: str):
    # Initialize an empty list to store DataFrames
    dfs = []

    # Loop through Parquet files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.parquet'):
            file_path = os.path.join(folder_path, file_name)
            
            # Read each Parquet file into a DataFrame
            df = pd.read_parquet(file_path)
            
            # Append the DataFrame to the list
            dfs.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    # View the combined DataFrame
    print(combined_df.head())  # View the first few rows
    print(combined_df.info())  # View information about the DataFrame


if __name__ == "__main__":
    folder_path = 'resources/data_files'
    view_data(folder_path)

