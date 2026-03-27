
Inventory API Endpoints

1. /getSingleProduct?product_id=ID
   Returns one product by ProductID.

2. /getAll
   Returns all products.

3. /addNew
   POST endpoint to add a new product.
   Required JSON fields:
   ProductID, Name, UnitPrice, StockQuantity, Description

4. /deleteOne?product_id=ID
   Deletes a product by ProductID.

5. /startsWith?letter=s
   Returns all products whose Name starts with the given letter.

6. /paginate?start_id=1&end_id=100
   Returns up to 10 products between the given ProductID values.

7. /convert?product_id=ID
   Returns the selected product price converted from USD to EUR.

FastAPI Docs:
http://127.0.0.1:8000/docs
