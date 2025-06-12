
from typing import Any, Optional
from datetime import datetime

class ProductEntity:
    """
    Represents a product entity with its attributes.
    This class is used to encapsulate product data and can be extended
    """
    
    def __init__(
        self,
        name: str,
        price: float,
        stock: int,
        category_id: str,
        status: str = "ACTIVE",
        product_id: Optional[str] = None,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        registration_date: Optional[datetime] = None,
        artisan_id: Optional[str] = None
    ) -> None:
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_url = image_url
        self.registration_date = (
            registration_date if registration_date else datetime.utcnow()
        )
        self.status = status
        self.artisan_id = artisan_id
        self.category_id = category_id
        
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
            registration_date=db_model.registration_date,
            status=db_model.status,
            artisan_id=db_model.artisan_id,
            image_url=db_model.image_url if db_model.image_url else None,
            category_id=db_model.category_id
        )
        
    def __repr__(self) -> str:
        return (
            f"ProductEntity(product_id={self.product_id!r}, name={self.name!r}, description={self.description!r}, "
            f"price={self.price!r}, stock={self.stock!r}, image_url={self.image_url!r}, "
            f"registration_date={self.registration_date!r}, status={self.status!r}, "
            f"artisan_id={self.artisan_id!r}, category_id={self.category_id!r})"
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.product_id}) - {self.status}"

    def __getattribute__(self, name: str) -> Any:
        return object.__getattribute__(self, name)
        