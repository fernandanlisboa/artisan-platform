from abc import ABC, abstractmethod
from app.domain.models.product import ProductEntity
from typing import Optional

class IProductRepository(ABC):
    """
    Interface (Abstract Base Class) for Product data access operations.
    Defines the contract for interacting with the 'products' table.
    """
    
    @abstractmethod
    def create_artisan_product(self, product_entity: ProductEntity) -> ProductEntity:
        """
        Save a product to the repository.
        
        :param product_entity: ProductEntity instance to be saved.
        :return: The saved ProductEntity instance.
        """
        pass
