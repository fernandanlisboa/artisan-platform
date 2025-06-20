from abc import ABC, abstractmethod
from app.domain.models.product import ProductEntity
from typing import Optional

class IProductRepository(ABC):
    """
    Interface (Abstract Base Class) for Product data access operations.
    Defines the contract for interacting with the 'products' table.
    """
    
    @abstractmethod
    def create(self, product_entity: ProductEntity) -> ProductEntity:
        """
        Save a product to the repository.
        
        :param product_entity: ProductEntity instance to be saved.
        :return: The saved ProductEntity instance.
        """
        pass
    
    @abstractmethod
    def get_product_by_id(self, product_id: str) -> Optional[ProductEntity]:
        """
        Retrieve a product by its ID.
        
        :param product_id: ID of the product to retrieve.
        :return: ProductEntity instance if found, None otherwise.
        """
        pass

    @abstractmethod
    def get_artisan_product_by_name(self, artisan_id: str, product_name: str) -> Optional[ProductEntity]:
        """
        Retrieve a product by artisan ID and product name.
        
        :param artisan_id: ID of the artisan.
        :param product_name: Name of the product to retrieve.
        :return: ProductEntity instance if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def find_by_artisan_id(self, artisan_id: str) -> list[ProductEntity]:
        """
        Find all products associated with a specific artisan ID.
        
        :param artisan_id: ID of the artisan whose products are to be retrieved.
        :return: List of ProductEntity instances associated with the artisan.
        """
        pass