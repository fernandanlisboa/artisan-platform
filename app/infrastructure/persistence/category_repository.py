
from app.domain.repositories.category_repository_interface import ICategoryRepository
from app.domain.models.category import CategoryEntity
from app.infrastructure.persistence.models_db.category_db_model import CategoryDBModel
from app.extensions import SessionLocal
from typing import Optional

class CategoryRepository(ICategoryRepository):
    """
    Concrete implementation of the ICategoryRepository interface.
    This class handles the persistence logic for CategoryEntity instances.
    """
    def __init__(self):
        super().__init__()

    def create(self, category: CategoryEntity) -> CategoryEntity:
        """
        Creates a new Category in the database and converts it to a pure domain entity.
        """
        category_db_model = CategoryDBModel.from_entity(category)
        session = SessionLocal()
        try:
            session.add(category_db_model)
            session.commit()
            return CategoryEntity.from_db_model(category_db_model)
        except Exception as e:
            print(f"Error saving category: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_by_id(self, category_id: str) -> Optional[CategoryEntity]:
        """
        Gets a Category by ID and converts it to a pure domain entity.
        """
        session = SessionLocal()
        try:
            category_db_model = session.get(CategoryDBModel, category_id)
            if category_db_model:
                return CategoryEntity.from_db_model(category_db_model)
            return None
        finally:
            session.close()