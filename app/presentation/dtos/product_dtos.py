from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

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
    category_id: str = Field(..., description="Category of the product")
    image_url: Optional[str] = Field(None, description="Image URL of the product")