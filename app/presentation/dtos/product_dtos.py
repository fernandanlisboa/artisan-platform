from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class CategoryDTO(BaseModel):
    """
    Data Transfer Object for Category.
    Used to transfer category data between layers.
    """
    model_config = ConfigDict(
        extra='forbid',  # Forbid extra fields
        validate_assignment=True,  # Validate on assignment
        protected_namespaces=(),  # No protected namespaces
        arbitrary_types_allowed=True  # Allow arbitrary types
    )

    category_id: Optional[int] = Field(None, description="ID of the category")
    name: str = Field(..., description="Name of the category")
    description: Optional[str] = Field(None, description="Description of the category")

class RegisterProductRequest(BaseModel):
    """
    Data Transfer Object for Product.
    Used to transfer product data between layers.
    """
    model_config = ConfigDict(
        extra='forbid',  # Forbid extra fields
        validate_assignment=True,  # Validate on assignment
        protected_namespaces=(),  # No protected namespaces
        arbitrary_types_allowed=True  # Allow arbitrary types
    )

    name: str = Field(..., description="Name of the product")
    description: str = Field(..., description="Description of the product")
    price: float = Field(..., description="Price of the product")
    stock: Optional[int] = Field(..., description="Stock quantity of the product")
    category_id: str = Field(..., description="Category ID of the registered product")
    image_url: Optional[str] = Field(None, description="Image URL of the product")
    
class ResponseRegisterProduct(BaseModel):
    """
    Response DTO for Product registration.
    Used to return product data after registration.
    """
    model_config = ConfigDict(
        extra='forbid',  # Forbid extra fields
        validate_assignment=True,  # Validate on assignment
        protected_namespaces=(),  # No protected namespaces
        arbitrary_types_allowed=True  # Allow arbitrary types
    )

    product_id: str = Field(..., description="ID of the registered product")
    name: str = Field(..., description="Name of the registered product")
    description: str = Field(..., description="Description of the registered product")
    price: float = Field(..., description="Price of the registered product")
    stock: int = Field(..., description="Stock quantity of the registered product")
    artisan_id: str = Field(..., description="ID of the artisan who registered the product")
    image_url: Optional[str] = Field(None, description="Image URL of the registered product")
    registration_date: datetime = Field(..., description="Registration date of the product")
    status: str = Field(..., description="Status of the registered product (e.g., active, inactive)")
    category: CategoryDTO = Field(..., description="Category of the registered product")
    
    @classmethod
    def from_domain_entities(cls, product, category):
        """
        Create a ResponseRegisterProduct instance from domain entities.
        
        :param product: The product entity.
        :param category: The category entity.
        :return: An instance of ResponseRegisterProduct.
        """
        return cls(
            product_id=product.product_id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            image_url=product.image_url,
            registration_date=product.registration_date,
            status=product.status,
            artisan_id=product.artisan_id,
            category=CategoryDTO(
                category_id=category.category_id,
                name=category.name,
                description=category.description
            )
        )