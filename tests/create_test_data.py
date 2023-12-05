import pandas as pd
import os
import random


def create_test_parquet(original_folder, test_file_path, row_count=50, seed=42):
    random.seed(seed)  # Set the seed for reproducibility

    # List all Parquet files in the specified directory
    all_files = [os.path.join(original_folder, file) for file in os.listdir(original_folder) if file.endswith('.parquet')]

    # Read and sample data from each file
    sampled_data_frames = []
    for file in all_files:
        df = pd.read_parquet(file)
        sampled_df = df.sample(row_count, replace=True, random_state=random.randint(0, 10000))
        sampled_data_frames.append(sampled_df)

    # Concatenate all samples into a single DataFrame
    combined_sampled_data = pd.concat(sampled_data_frames)

    # Write the sampled data to a new Parquet file
    combined_sampled_data.to_parquet(test_file_path)


if __name__ == "__main__":
    original_folder_path = './resources/data_files'
    test_parquet_file_path = 'tests/test_data/test_parquet_file.parquet'

    # Create the test Parquet file
    create_test_parquet(original_folder_path, test_parquet_file_path)
