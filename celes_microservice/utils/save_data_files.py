import os
import pandas as pd
import sqlite3


def preprocess_data(df):
    for col in df.columns:
        if df[col].dtype != 'float64':
            df[col] = df[col].astype(str)
    return df


def save_parquet_files(folder: str):
    conn = sqlite3.connect('celes.db')
    combined_df = pd.DataFrame()  # Create an empty DataFrame for combining data

    for file_name in os.listdir(folder):
        if file_name.endswith('.parquet'):
            file_path = os.path.join(folder, file_name)
            df = pd.read_parquet(file_path)
            df = preprocess_data(df)
            combined_df = pd.concat([combined_df, df], ignore_index=True)  # Concatenate data
            
    combined_df.to_sql('celes', conn, index=False, if_exists='replace')  # Save to SQLite as one table

    conn.close()


if __name__ == "__main__":
    folder_path = 'resources/data_files'
    save_parquet_files(folder_path)
