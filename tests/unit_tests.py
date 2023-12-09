from fastapi.testclient import TestClient 
import pandas as pd
from celes_microservice.api_queries import app 
import firebase_admin
from firebase_admin import credentials
import os
import celes_microservice.firebase_auth


client = TestClient(app)


sample_data = {
    "valid_employee_key": "1|17542",
    "invalid_employee_key": "123456X",
    "valid_product_key": "1|62481",
    "invalid_product_key": "123456Y",
    "valid_store_key": "1|004",
    "invalid_store_key": "1234Z",
    "from_date": "2022-10-01",
    "to_date": "2023-12-04"
}

TEST_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNhM2JkODk4ZGE1MGE4OWViOWUxY2YwYjdhN2VmZTM1OTNkNDEwNjgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY2VsZXMtcXVlcmllcyIsImF1ZCI6ImNlbGVzLXF1ZXJpZXMiLCJhdXRoX3RpbWUiOjE3MDE5NDE0NzMsInVzZXJfaWQiOiJRUDhPdElHeUFZZFNwbzhNV0poaHh5R3A5eDUyIiwic3ViIjoiUVA4T3RJR3lBWWRTcG84TVdKaGh4eUdwOXg1MiIsImlhdCI6MTcwMTk0MTQ3MywiZXhwIjoxNzAxOTQ1MDczLCJlbWFpbCI6InNhbW15QHRlc3QuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInNhbW15QHRlc3QuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.Cd6SEJoSsOStS7J30aG3eOBcrqnkmUMGkZk11diHiih6n78woMRbB5Xr1Q1SYl7ZppIxqsli1wtFCdmRKXkuT5dvZ7Rfz6ltaJl-B2SLcc6DkuKeC9GWW8qYXGgpTtUTPbn9Ry6j5yT4bVdjZQNdY6-yAu5-JjpUPmQSrAMkw2IqnMV-qalnfgkl6g4K9PMM-zZuRpCs8Gu7--gko_YqQwI8H0dgMaAPGVsF8U6sBDYXLDFvmZZ-yxUGCUntrwfLYlNUe4DQjofZN0lLybYMHwuZqz6bkftFdMxJK8CVNtgo7pDgWi3Tm9fx7vjI55kwGh4nPPhwvDQrdpY6ucOckw"

# firebase initialization code
if not firebase_admin._apps and not os.getenv("TEST_ENV"):
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)


def test_sales_per_employee_valid():
    #response = client.get(f"/sales_per_employee/{sample_data['valid_employee_key']}?from_date={sample_data['from_date']}&to_date={sample_data['to_date']}")
    response = client.get(
        f"/sales_per_employee/{sample_data['valid_employee_key']}?from_date={sample_data['from_date']}&to_date={sample_data['to_date']}",
        headers={
            "Authorization": f"Bearer {TEST_TOKEN}",
        },
    )
    assert response.status_code == 200
    try:
        df = pd.DataFrame(response.json())
        assert not df.empty
    except Exception as e:
        assert False, f"Failed to convert JSON to DataFrame: {e}"


def test_sales_per_employee_invalid():
    response = client.get(f"/sales_per_employee/{sample_data['invalid_employee_key']}?from_date={sample_data['from_date']}&to_date={sample_data['to_date']}")
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]


def test_sales_per_product_valid():
    response = client.get(f"/sales_per_product/{sample_data['valid_product_key']}?from_date={sample_data['from_date']}&to_date={sample_data['to_date']}")
    assert response.status_code == 200
    try:
        df = pd.DataFrame(response.json())
        assert not df.empty
    except Exception as e:
        assert False, f"Failed to convert JSON to DataFrame: {e}"


def test_sales_by_product_invalid():
    response = client.get(f"/sales_per_product/{sample_data['invalid_product_key']}?from_date={sample_data['from_date']}&to_date={sample_data['to_date']}")
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]


def test_sales_by_store_valid():
    response = client.get(f"/sales_per_store/{sample_data['valid_store_key']}?from_date={sample_data['from_date']}&to_date={sample_data['to_date']}")
    assert response.status_code == 200
    try:
        df = pd.DataFrame(response.json())
        assert not df.empty
    except Exception as e:
        assert False, f"Failed to convert JSON to DataFrame: {e}"


def test_sales_by_store_invalid():
    response = client.get(f"/sales_per_store/{sample_data['invalid_store_key']}?from_date={sample_data['from_date']}&to_date={sample_data['to_date']}")
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
