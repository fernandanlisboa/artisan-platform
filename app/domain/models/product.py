
from typing import Any
from datetime import datetime

class ProductEntity:
    """
    Represents a product entity with its attributes.
    This class is used to encapsulate product data and can be extended
    """
    
    def __init__(self, name: str, price: float, stock: int, status: str = "ACTIVE", product_id: str = None, description: str = None, image_url: str = None, registration_date: datetime) -> None:
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_url = image_url
        self.registration_date = registration_date if registration_date else datetime.utcnow()
        self.status = status
        
        
    
    def __repr__(self) -> str:
        pass
    
    def __str__(self) -> str:
        pass
    
    def __getattribute__(self, name: str) -> Any:
        pass