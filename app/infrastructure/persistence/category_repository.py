
from app.domain.repositories.category_repository_interface import ICategoryRepository
from app.domain.models.category import CategoryEntity
from app.infrastructure.persistence.models_db.category_db_model import CategoryDBModel
from app import db
from typing import Optional

class CategoryRepository(ICategoryRepository):
    """
    Concrete implementation of the ICategoryRepository interface.
    This class handles the persistence logic for CategoryEntity instances.
    """
    def __init__(self):
        super().__init__()

    def get_by_id(self, category_id: str) -> Optional[CategoryEntity]:
        """
        Gets a Category by ID and converts it to a pure domain entity.
        """
        category_db_model = CategoryDBModel.query.get(category_id)
        if category_db_model:
            return CategoryEntity.from_db_model(category_db_model)
        return None