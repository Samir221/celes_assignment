import os
from fastapi import FastAPI
import pyarrow.parquet as pq
import pyarrow as pa
import uvicorn


app = FastAPI()

# Path to the directory containing the Parquet files
parquet_folder_path = "../resources/data_files"

# List all files in the specified directory
all_files = os.listdir(parquet_folder_path)

# Filter out only the Parquet files
parquet_file_paths = [os.path.join(parquet_folder_path, file) for file in all_files if file.endswith('.parquet')]

record_batches = []
for file_path in parquet_file_paths:
    table = pq.read_table(file_path)
    record_batches.extend(table.to_batches())

# Concatenate the record batches into a single table
combined_table = pa.Table.from_batches(record_batches)


# Endpoint to view sales in a period per employee
@app.get("/sales_per_employee/{key}")
def sales_per_employee(key: str):
    sales_data = combined_table.filter(f"KeyEmployee == '{key}'").to_pydict()
    return {"sales_per_employee": sales_data}


# Endpoint to view sales in a period by product
@app.get("/sales_by_product/{key}")
def sales_by_product(key: str):
    sales_data = combined_table.filter(f"KeyProduct == '{key}'").to_pydict()
    return {"sales_by_product": sales_data}


# Endpoint to view sales in a period by store
@app.get("/sales_by_store/{key}")
def sales_by_store(key: str):
    sales_data = combined_table.filter(f"KeyStore == '{key}'").to_pydict()
    return {"sales_by_store": sales_data}


# Endpoint to view total and average sales by store
@app.get("/total_avg_sales_by_store/{key}")
def total_avg_sales_by_store(key: str):
    filtered_table = combined_table.filter(f"KeyStore == '{key}'")
    sales_data = filtered_table.groupby("KeyStore").agg({"Amount": ["sum", "mean"]}).to_pydict()
    return {"total_avg_sales_by_store": sales_data}


# Endpoint to view total and average sales by product
@app.get("/total_avg_sales_by_product/{key}")
def total_avg_sales_by_product(key: str):
    filtered_table = combined_table.filter(f"KeyProduct == '{key}'")
    sales_data = filtered_table.groupby("KeyProduct").agg({"Amount": ["sum", "mean"]}).to_pydict()
    return {"total_avg_sales_by_product": sales_data}


# Endpoint to view total and average sales per employee
@app.get("/total_avg_sales_per_employee/{key}")
def total_avg_sales_per_employee(key: str):
    filtered_table = combined_table.filter(f"KeyEmployee == '{key}'")
    sales_data = filtered_table.groupby("KeyEmployee").agg({"Amount": ["sum", "mean"]}).to_pydict()
    return {"total_avg_sales_per_employee": sales_data}

