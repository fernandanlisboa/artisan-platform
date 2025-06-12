
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
        
    @classmethod
    def from_db_model(cls, db_model: Any) -> 'ProductEntity':
        """
        Creates a ProductEntity instance from a database model.
        
        :param db_model: The database model instance containing product data.
        :return: An instance of ProductEntity.
        """
        return cls(
            product_id=db_model.product_id,
            name=db_model.name,
            description=db_model.description,
            price=db_model.price,
            stock=db_model.stock,
            image_url=db_model.image_url,
            registration_date=db_model.registration_date,
            status=db_model.status
        )
    
    def __repr__(self) -> str:
        pass
    
    def __str__(self) -> str:
        pass
    
    def __getattribute__(self, name: str) -> Any:
        pass