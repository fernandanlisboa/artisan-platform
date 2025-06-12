from abc import ABC, abstractmethod
from app.domain.models.category import CategoryEntity
from typing import Optional

#interface
class ICategoryRepository(ABC):
    """
    Interface (Abstract Base Class) for Category data access operations.
    Defines the contract for interacting with the 'categories' table.
    """
    
    @abstractmethod
    def create_category(self, category_entity: CategoryEntity) -> CategoryEntity:
        """
        Save a category to the repository.
        
        :param category_entity: CategoryEntity instance to be saved.
        :return: The saved CategoryEntity instance.
        """
        pass
    