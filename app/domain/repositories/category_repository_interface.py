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
    def create(self, category: CategoryEntity) -> CategoryEntity:
        """Creates a new Category entity."""
        pass
    
    @abstractmethod
    def get_by_id(self, category_id: str) -> Optional[CategoryEntity]:
        """Gets a Category entity by its ID."""
        pass