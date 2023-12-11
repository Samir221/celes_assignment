from fastapi import Depends, FastAPI
import pandas as pd
from fastapi import HTTPException
from datetime import datetime
from celes_microservice.firebase_auth import validate_token


app = FastAPI()


# Path to the directory containing the Parquet files
parquet_folder_path = "./resources/data_files"

full_df = pd.read_parquet(parquet_folder_path, engine='auto')


# Endpoint to view sales in a period by employee
@app.get("/sales_per_employee/{key}")
async def sales_per_employee(key: str, from_date: str, to_date: str, user_id: str = Depends(validate_token)):
    from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    filtered_df = full_df[(full_df['KeyEmployee'] == key) & (full_df['KeyDate'] >= from_date) & (full_df['KeyDate'] <= to_date)]

    if len(filtered_df) == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    json_data = filtered_df.to_dict(orient='records')
    
    return json_data


# Endpoint to view sales in a period by product
@app.get("/sales_per_product/{key}")
def sales_per_product(key: str, from_date: str, to_date: str, user_id: str = Depends(validate_token)):
    from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    filtered_df = full_df[(full_df['KeyProduct'] == key) & (full_df['KeyDate'] >= from_date) & (full_df['KeyDate'] <= to_date)]

    if len(filtered_df) == 0:
        raise HTTPException(status_code=404, detail="Not Found")
    
    json_data = filtered_df.to_dict(orient='records')
    
    return json_data
    

# Endpoint to view sales in a period by store
@app.get("/sales_per_store/{key}")
def sales_per_store(key: str, from_date: str, to_date: str, user_id: str = Depends(validate_token)):
    from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    filtered_df = full_df[(full_df['KeyStore'] == key) & (full_df['KeyDate'] >= from_date) & (full_df['KeyDate'] <= to_date)]

    if len(filtered_df) == 0:
        raise HTTPException(status_code=404, detail="Not Found")
    
    json_data = filtered_df.to_dict(orient='records')
    
    return json_data


# Endpoint to view total and average sales by store
@app.get("/total_avg_sales_by_store/{key}")
def total_avg_sales_by_store(key: str, user_id: str = Depends(validate_token)):

    filtered_df = full_df[full_df['KeyStore'] == key] 

    if len(filtered_df) == 0:
        raise HTTPException(status_code=404, detail="Not Found")

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
def total_avg_sales_by_product(key: str, user_id: str = Depends(validate_token)):

    filtered_df = full_df[full_df['KeyProduct'] == key] 

    if len(filtered_df) == 0:
        raise HTTPException(status_code=404, detail="Not Found")
    
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
def total_avg_sales_by_employee(key: str, user_id: str = Depends(validate_token)):

    filtered_df = full_df[full_df['KeyEmployee'] == key] 

    if len(filtered_df) == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    sum_amount = filtered_df['Amount'].sum()
    mean_amount = filtered_df['Amount'].mean()

    # Prepare the response data
    sales_data = {
        "sum_amount": sum_amount,
        "mean_amount": mean_amount
    }
    return {"total_avg_sales_by_store": sales_data}
