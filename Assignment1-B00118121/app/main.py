# Import FastAPI to create the web application
# Import HTTPException to return error responses with specific status codes
# Import Query to allow us to validate query parameters passed into the URLs
from fastapi import FastAPI, HTTPException, Query

# Import the Product model we defined in models.py for validating new product data
from app.models import Product

# Import the products_collection so we can interact with the MongoDB database
from app.database import products_collection

# Import requests so we can call the external currency exchange rate API
import requests

# Create the FastAPI application instance
app = FastAPI()


# Home endpoint 

# This is the root URL of the API
# Returns a simple message to confirm the API is running
@app.get("/")
def home():
    return {"message": "Inventory API is running"}


# Health check endpoint 

# A simple health check endpoint that returns ok
# Useful for monitoring tools to check if the API is still alive
@app.get("/health")
def health():
    return {"status": "ok"}


# Get a single product 

# Accepts a product_id as a query parameter e.g. /getSingleProduct?product_id=1001
# Query(..., gt=0) means the parameter is required and must be greater than 0
# {"_id": 0} tells MongoDB to exclude the internal _id field from the result
@app.get("/getSingleProduct")
def get_single_product(product_id: int = Query(..., gt=0)):

    # Search the database for a product with the matching ProductID
    product = products_collection.find_one({"ProductID": product_id}, {"_id": 0})

    # If no product was found, return a 404 Not Found error
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Return the product as a JSON response
    return product


# Get all products 

# Returns every product in the database as a list
# {"_id": 0} excludes the MongoDB internal _id field from each result
@app.get("/getAll")
def get_all():
    return list(products_collection.find({}, {"_id": 0}))


# Add a new product 

# Accepts a full Product object in the request body
# Pydantic automatically validates all fields before this function runs
@app.post("/addNew")
def add_new(product: Product):

    # Check if a product with the same ProductID already exists in the database
    existing = products_collection.find_one({"ProductID": product.ProductID})

    # If a duplicate is found, return a 400 Bad Request error
    if existing:
        raise HTTPException(status_code=400, detail="ProductID already exists")

    # Convert the Pydantic model to a dictionary and insert it into the database
    products_collection.insert_one(product.dict())

    # Return a success message
    return {"message": "Product added successfully"}


# Delete a product

# Accepts a product_id as a query parameter e.g. /deleteOne?product_id=1001
# Query(..., gt=0) means the parameter is required and must be greater than 0
@app.delete("/deleteOne")
def delete_one(product_id: int = Query(..., gt=0)):

    # Attempt to delete the product with the matching ProductID
    result = products_collection.delete_one({"ProductID": product_id})

    # deleted_count will be 0 if no product with that ID was found
    # Return a 404 Not Found error in that case
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    # Return a success message confirming the deletion
    return {"message": "Product deleted successfully"}


# Find products starting with a letter 

# Accepts a single letter as a query parameter e.g. /startsWith?letter=s
# min_length=1 and max_length=1 ensures exactly one character is passed in
@app.get("/startsWith")
def starts_with(letter: str = Query(..., min_length=1, max_length=1)):

    # Use a MongoDB regex query to find all products whose Name starts with the given letter
    # ^ means starts with
    # $options: "i" makes the search case-insensitive (so S and s both work)
    return list(
        products_collection.find(
            {"Name": {"$regex": f"^{letter}", "$options": "i"}},
            {"_id": 0}
        )
    )


# Paginate products by ID range 

# Accepts a start_id and end_id as query parameters e.g. /paginate?start_id=1010&end_id=1020
# Returns up to 10 products whose ProductID falls between start_id and end_id
@app.get("/paginate")
def paginate(
    start_id: int = Query(..., gt=0),
    end_id:   int = Query(..., gt=0)
):
    # $gte means greater than or equal to start_id
    # $lte means less than or equal to end_id
    # .sort() orders the results by ProductID in ascending order
    # .limit(10) ensures no more than 10 products are returned at once
    return list(
        products_collection.find(
            {"ProductID": {"$gte": start_id, "$lte": end_id}},
            {"_id": 0}
        ).sort("ProductID", 1).limit(10)
    )


# Convert product price from USD to EUR 

# Accepts a product_id as a query parameter e.g. /convert?product_id=1001
# Fetches the current USD to EUR exchange rate from an external API
# and returns the product price converted into euros
@app.get("/convert")
def convert(product_id: int = Query(..., gt=0)):

    # Look up the product in the database by its ProductID
    product = products_collection.find_one({"ProductID": product_id}, {"_id": 0})

    # If no product was found, return a 404 Not Found error
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Call the external exchange rate API to get the latest USD rates
    # timeout=10 means the request will give up after 10 seconds if no response
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)

    # Parse the JSON response into a Python dictionary
    data = response.json()

    # Extract the EUR exchange rate from the rates section of the response
    eur_rate = data["rates"]["EUR"]

    # Multiply the product's USD price by the exchange rate to get the EUR price
    # round(..., 2) rounds the result to 2 decimal places
    eur_price = round(product["UnitPrice"] * eur_rate, 2)

    # Return all the price information including both currencies and the exchange rate used
    return {
        "ProductID":    product["ProductID"],
        "Name":         product["Name"],
        "PriceUSD":     product["UnitPrice"],
        "PriceEUR":     eur_price,
        "ExchangeRate": eur_rate
    }