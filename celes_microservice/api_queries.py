from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi import status
import uvicorn


app = FastAPI()


# Path to the directory containing the Parquet files
parquet_folder_path = "../resources/data_files"

full_df = pd.read_parquet(parquet_folder_path, engine='auto')


# Endpoint to view sales in a period per employee
@app.get("/sales_per_employee/{key}")
def sales_per_employee(key):
    print(f"Received key: {key}")

    # Check for empty key
    if key == " ":
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": "Blank Key"})

    filtered_df = full_df[full_df['KeyEmployee'] == key] 

    # Check if the filtered table is empty
    if len(filtered_df) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not Found"})
    
    # Convert DataFrame to a list of dictionaries (JSON serializable)
    json_data = filtered_df.to_dict(orient='records')
    
    return json_data 


# Endpoint to view sales in a period by product
@app.get("/sales_by_product/{key}")
def sales_by_product(key: str):
    # Check for empty key
    if key == " ":
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": "Blank Key"})
    
    filtered_df = full_df[full_df['KeyProduct'] == key] 
    
    # Check if the filtered table is empty
    if len(filtered_df) == 0:
        print("HELLLOOOOOOO")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not Found"})

    # Convert DataFrame to a list of dictionaries (JSON serializable)
    json_data = filtered_df.to_dict(orient='records')
    
    return json_data 
    

# Endpoint to view sales in a period by store
@app.get("/sales_by_store/{key}")
def sales_by_store(key: str):
    # Check for empty key
    if key == " ":
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": "Blank Key"})
    
    filtered_df = full_df[full_df['KeyStore'] == key] 
    
    # Check if the filtered table is empty
    if len(filtered_df) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not Found"})

    # Convert DataFrame to a list of dictionaries (JSON serializable)
    json_data = filtered_df.to_dict(orient='records')
    
    return json_data 


# Endpoint to view total and average sales by store
@app.get("/total_avg_sales_by_store/{key}")
def total_avg_sales_by_store(key: str):

    filtered_df = full_df[full_df['KeyStore'] == key] 

    # Check if the filtered table is empty
    if len(filtered_df) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not Found"})

    # Perform aggregation operations separately
    sum_amount = filtered_df['Amount'].sum()
    mean_amount = filtered_df['Amount'].mean()

    # Prepare the response data
    sales_data = {
        "sum_amount": sum_amount,
        "mean_amount": mean_amount
    }

    return {"total_avg_sales_by_store": sales_data}


# Endpoint to view total and average sales by product
@app.get("/total_avg_sales_by_product/{key}")
def total_avg_sales_by_product(key: str):

    filtered_df = full_df[full_df['KeyProduct'] == key] 

    # Check if the filtered table is empty
    if len(filtered_df) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not Found"})

    # Perform aggregation operations separately
    sum_amount = filtered_df['Amount'].sum()
    mean_amount = filtered_df['Amount'].mean()

    # Prepare the response data
    sales_data = {
        "sum_amount": sum_amount,
        "mean_amount": mean_amount
    }

    return {"total_avg_sales_by_store": sales_data}


# Endpoint to view total and average sales by employee
@app.get("/total_avg_sales_by_employee/{key}")
def total_avg_sales_by_employee(key: str):

    filtered_df = full_df[full_df['KeyEmployee'] == key] 

    # Check if the filtered table is empty
    if len(filtered_df) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not Found"})

    # Perform aggregation operations separately
    sum_amount = filtered_df['Amount'].sum()
    mean_amount = filtered_df['Amount'].mean()

    # Prepare the response data
    sales_data = {
        "sum_amount": sum_amount,
        "mean_amount": mean_amount
    }

    return {"total_avg_sales_by_store": sales_data}
