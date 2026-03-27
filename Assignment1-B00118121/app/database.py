# Import MongoClient from the pymongo library to allow us to connect to MongoDB
from pymongo import MongoClient

# Connect to the local MongoDB instance running on the default port 27017
client = MongoClient("mongodb://localhost:27017/")

# Select the database named 'inventory_db' (created automatically if it doesn't exist)
db = client["inventory_db"]

# Select the 'products' collection inside the database (also created automatically if it doesn't exist)
products_collection = db["products"]