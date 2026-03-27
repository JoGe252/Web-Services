# Import the csv module to allow us to read CSV files
import csv

# Import MongoClient from pymongo to allow us to connect to MongoDB
from pymongo import MongoClient

# Connect to the local MongoDB instance running on the default port 27017
client = MongoClient("mongodb://localhost:27017/")

# Select the database named 'inventory_db'
db = client["inventory_db"]

# Select the 'products' collection inside the database
products_collection = db["products"]

# Delete all existing documents in the collection before importing
# This ensures we don't end up with duplicate products if the script is run more than once
products_collection.delete_many({})

# Open the CSV file for reading
# newline="" prevents extra blank lines being added on Windows
# encoding="utf-8" ensures special characters are handled correctly
with open("products.csv", newline="", encoding="utf-8") as csvfile:

    # DictReader reads each row of the CSV as a dictionary
    # where the keys are taken from the header row of the file
    reader = csv.DictReader(csvfile)

    # Create an empty list to store all the documents before inserting them
    documents = []

    # Loop through every row in the CSV file
    for row in reader:

        # Build a dictionary for each product, converting each field to the correct data type
        # int() is used for ProductID and StockQuantity as they are whole numbers
        # float() is used for UnitPrice as it can have decimal places
        # Name and Description are left as strings
        document = {
            "ProductID": int(row["ProductID"]),
            "Name": row["Name"],
            "UnitPrice": float(row["UnitPrice"]),
            "StockQuantity": int(row["StockQuantity"]),
            "Description": row["Description"]
        }

        # Add the completed document to the list
        documents.append(document)

    # Only insert if the list is not empty
    # insert_many() inserts all documents in a single database operation, which is faster than inserting one at a time
    if documents:
        products_collection.insert_many(documents)

# Print a confirmation message so the user knows the import completed successfully
print("CSV imported into MongoDB successfully.")