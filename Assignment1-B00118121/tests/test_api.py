# Import TestClient from FastAPI which allows us to send test requests
# to our API without needing to run a real server
from fastapi.testclient import TestClient

# Import the FastAPI app instance from our main application file
from app.main import app

# Create a test client using our app
# This client will be used in every test to send requests to the API
client = TestClient(app)


# Test the home endpoint 

# Test that the root URL returns a 200 OK response
# This confirms the API is running and the home endpoint is reachable
def test_home():
    response = client.get("/")
    assert response.status_code == 200


# Test the health check endpoint 

# Test that the health endpoint returns 200 OK
# Also checks that the response body contains "status": "ok"
# confirming the health check is returning the correct message
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# Test the get all products endpoint 

# Test that the /getAll endpoint returns a 200 OK response
# Also checks that the response is a list
# confirming all products are being returned in the correct format
def test_get_all():
    response = client.get("/getAll")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test the get single product endpoint 

# Test that the /getSingleProduct endpoint handles a request correctly
# We accept either 200 OK (product was found) or 404 Not Found (product does not exist)
# because the test database may or may not have a product with ID 1
def test_get_single_product():
    response = client.get("/getSingleProduct?product_id=1")
    assert response.status_code in [200, 404]


# Test the startsWith endpoint 

# Test that the /startsWith endpoint returns a 200 OK response
# when passed the letter s
# This confirms the endpoint is reachable and handles the letter parameter correctly
def test_starts_with():
    response = client.get("/startsWith?letter=s")
    assert response.status_code == 200


# Test the paginate endpoint 

# Test that the /paginate endpoint returns a 200 OK response
# when given a start_id of 1 and an end_id of 100
# Also checks that the result is a list confirming
# the products are returned in the correct format
def test_paginate():
    response = client.get("/paginate?start_id=1&end_id=100")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test the convert endpoint 

# Test that the /convert endpoint handles a request correctly
# We accept either 200 OK (product was found and price was converted)
# or 404 Not Found (product does not exist in the database)
# because the test database may or may not have a product with ID 1
def test_convert():
    response = client.get("/convert?product_id=1")
    assert response.status_code in [200, 404]