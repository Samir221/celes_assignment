from fastapi.testclient import TestClient
from celes_microservice.api_queries import app


client = TestClient(app)


# Tests for /sales_per_employee/{key} endpoint
def test_sales_per_employee_valid():
    response = client.get("/sales_per_employee/valid_key")
    assert response.status_code == 200
    assert "sales_per_employee" in response.json()

def test_sales_per_employee_invalid():
    response = client.get("/sales_per_employee/invalid_key")
    assert response.status_code == 404

def test_sales_per_employee_edge_case():
    response = client.get("/sales_per_employee/special@key#")
    assert response.status_code == 200

def test_sales_per_employee_empty():
    response = client.get("/sales_per_employee/empty_key")
    assert response.status_code == 200
    assert response.json() == {"sales_per_employee": {}}

def test_sales_per_employee_wrong_format():
    response = client.get("/sales_per_employee/123")
    assert response.status_code == 422

# Tests for /sales_by_product/{key} endpoint
def test_sales_by_product_valid():
    response = client.get("/sales_by_product/valid_product_key")
    assert response.status_code == 200
    assert "sales_by_product" in response.json()

def test_sales_by_product_invalid():
    response = client.get("/sales_by_product/invalid_product_key")
    assert response.status_code == 404

def test_sales_by_product_edge_case():
    response = client.get("/sales_by_product/special@key#")
    assert response.status_code == 200

def test_sales_by_product_empty():
    response = client.get("/sales_by_product/empty_product_key")
    assert response.status_code == 200
    assert response.json() == {"sales_by_product": {}}

def test_sales_by_product_wrong_format():
    response = client.get("/sales_by_product/123")
    assert response.status_code == 422

# Tests for /sales_by_store/{key} endpoint
def test_sales_by_store_valid():
    response = client.get("/sales_by_store/valid_store_key")
    assert response.status_code == 200
    assert "sales_by_store" in response.json()

def test_sales_by_store_invalid():
    response = client.get("/sales_by_store/invalid_store_key")
    assert response.status_code == 404

def test_sales_by_store_edge_case():
    response = client.get("/sales_by_store/special@key#")
    assert response.status_code == 200

def test_sales_by_store_empty():
    response = client.get("/sales_by_store/empty_store_key")
    assert response.status_code == 200
    assert response.json() == {"sales_by_store": {}}

def test_sales_by_store_wrong_format():
    response = client.get("/sales_by_store/123")
    assert response.status_code == 422

# Tests for /total_avg_sales_by_store/{key} endpoint
def test_total_avg_sales_by_store_valid():
    response = client.get("/total_avg_sales_by_store/valid_store_key")
    assert response.status_code == 200
    assert "total_avg_sales_by_store" in response.json()

def test_total_avg_sales_by_store_invalid():
    response = client.get("/total_avg_sales_by_store/invalid_store_key")
    assert response.status_code == 404

def test_total_avg_sales_by_store_edge_case():
    response = client.get("/total_avg_sales_by_store/special@key#")
    assert response.status_code == 200

def test_total_avg_sales_by_store_empty():
    response = client.get("/total_avg_sales_by_store/empty_store_key")
    assert response.status_code == 200
    assert response.json() == {"total_avg_sales_by_store": {}}

def test_total_avg_sales_by_store_wrong_format():
    response = client.get("/total_avg_sales_by_store/123")
    assert response.status_code == 422

# Tests for /total_avg_sales_by_product/{key} endpoint
def test_total_avg_sales_by_product_valid():
    response = client.get("/total_avg_sales_by_product/valid_product_key")
    assert response.status_code == 200
    assert "total_avg_sales_by_product" in response.json()

def test_total_avg_sales_by_product_invalid():
    response = client.get("/total_avg_sales_by_product/invalid_product_key")
    assert response.status_code == 404

def test_total_avg_sales_by_product_edge_case():
    response = client.get("/total_avg_sales_by_product/special@key#")
    assert response.status_code == 200

def test_total_avg_sales_by_product_empty():
    response = client.get("/total_avg_sales_by_product/empty_product_key")
    assert response.status_code == 200
    assert response.json() == {"total_avg_sales"}


# Sample Data for Tests
sample_data = {
    "valid_employee_key": "1|17542",  # Replace with actual valid data
    "invalid_employee_key": "XXXXX",
    "empty_key": "",
    "wrong_format_key": "1#17542",
    "valid_product_key": "1|43448",  # Replace with actual valid product data
    "invalid_product_key": "4|73248",
    "empty_product_key": "",
    "valid_store_key": "1|103",  # Replace with actual valid store data
    "invalid_store_key": "4|999",
    "empty_store_key": "",
}


# Helper function to perform tests
def run_test(endpoint, key, expected_status, expected_response=None):
    response = client.get(f"/{endpoint}/{key}")
    assert response.status_code == expected_status
    if expected_response is not None:
        assert response.json() == expected_response


# Tests for each endpoint
def test_endpoints():
    # /sales_per_employee/{key} endpoint
    run_test("sales_per_employee", "valid_key", 200, sample_data["valid_key"])
    run_test("sales_per_employee", "invalid_key", 404)
    run_test("sales_per_employee", "special_key", 200, sample_data["special_key"])
    run_test("sales_per_employee", "empty_key", 200, sample_data["empty_key"])
    run_test("sales_per_employee", "wrong_format_key", 422)

    # /sales_by_product/{key} endpoint
    run_test("sales_by_product", "valid_product_key", 200, sample_data["valid_product_key"])
    run_test("sales_by_product", "invalid_product_key", 404)
    run_test("sales_by_product", "special_key", 200, sample_data["special_key"])
    run_test("sales_by_product", "empty_product_key", 200, sample_data["empty_product_key"])
    run_test("sales_by_product", "wrong_format_key", 422)

    # Additional tests for other endpoints following the same pattern...
    # ...


# Execute the tests
if __name__ == "__main__":
    test_endpoints()