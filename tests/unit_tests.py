from fastapi.testclient import TestClient 
import sys
import pandas as pd
#sys.path.append(r'C:\Users\samir\tech_projects\celes_assignment')
from celes_microservice.api_queries import app 


client = TestClient(app)


sample_data = {
    "valid_employee_key": "1|17542",  
    "invalid_employee_key": "123456X",
    "valid_product_key": "1|43448",
    "invalid_product_key": "123456Y",
    "valid_store_key": "1|103",
    "invalid_store_key": "1234Z",
}


def test_sales_per_employee_valid():
    response = client.get("/sales_per_employee/" + sample_data["valid_employee_key"])
    assert response.status_code == 200
    try:
        df = pd.DataFrame(response.json())
        assert not df.empty
    except Exception as e:
        assert False, f"Failed to convert JSON to DataFrame: {e}"


def test_sales_per_employee_invalid():
    response = client.get("/sales_per_employee/" + sample_data["invalid_employee_key"])
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]


def test_sales_by_product_valid():
    response = client.get("/sales_by_product/" + sample_data["valid_product_key"])
    assert response.status_code == 200
    try:
        df = pd.DataFrame(response.json())
        assert not df.empty
    except Exception as e:
        assert False, f"Failed to convert JSON to DataFrame: {e}"


def test_sales_by_product_invalid():
    response = client.get("/sales_by_product/" + sample_data["invalid_product_key"])
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]


def test_sales_by_store_valid():
    response = client.get("/sales_by_store/" + sample_data["valid_store_key"])
    assert response.status_code == 200
    try:
        df = pd.DataFrame(response.json())
        assert not df.empty
    except Exception as e:
        assert False, f"Failed to convert JSON to DataFrame: {e}"


def test_sales_by_store_invalid():
    response = client.get("/sales_by_store/" + sample_data["invalid_store_key"])
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]


def test_total_avg_sales_by_store_valid():
    response = client.get("/total_avg_sales_by_store/" + sample_data["valid_store_key"])
    assert response.status_code == 200
    assert "total_avg_sales_by_store" in response.json()


def test_total_avg_sales_by_store_invalid():
    response = client.get("/total_avg_sales_by_store/" + sample_data["invalid_store_key"])
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]


def test_total_avg_sales_by_product_valid():
    response = client.get("/total_avg_sales_by_product/" + sample_data["valid_product_key"])
    assert response.status_code == 200
    assert "total_avg_sales_by_store" in response.json()


def test_total_avg_sales_by_product_invalid():
    response = client.get("/total_avg_sales_by_product/" + sample_data["invalid_product_key"])
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]  


def test_total_avg_sales_by_employee_valid():
    response = client.get("/total_avg_sales_by_store/" + sample_data["valid_store_key"])
    assert response.status_code == 200
    assert "total_avg_sales_by_store" in response.json()


def test_total_avg_sales_by_employee_invalid():
    response = client.get("/total_avg_sales_by_employee/" + sample_data["invalid_employee_key"])
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]    