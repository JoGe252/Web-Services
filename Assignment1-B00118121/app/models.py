# Import BaseModel from pydantic which all our data models must inherit from
# Import Field which allows us to add validation rules to each attribute
from pydantic import BaseModel, Field

# Define a Product class that inherits from BaseModel
# This acts as a blueprint that describes what a valid product looks like
# Pydantic will automatically validate any data passed in against these rules
class Product(BaseModel):

    # ProductID must be an integer
    # The ... means this field is required (cannot be left out)
    # gt=0 means the value must be greater than 0 (no negative IDs or zero allowed)
    ProductID: int = Field(..., gt=0)

    # Name must be a string
    # min_length=1 means the name cannot be empty
    Name: str = Field(..., min_length=1)

    # UnitPrice must be a float (decimal number)
    # gt=0 means the price must be greater than 0 (a product cannot be free or negative)
    UnitPrice: float = Field(..., gt=0)

    # StockQuantity must be an integer
    # ge=0 means the value must be greater than or equal to 0
    # (a product can have 0 stock, but cannot have a negative quantity)
    StockQuantity: int = Field(..., ge=0)

    # Description must be a string
    # min_length=1 means the description cannot be empty
    Description: str = Field(..., min_length=1)