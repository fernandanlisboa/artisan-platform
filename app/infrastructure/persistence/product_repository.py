from app.domain.repositories.product_repository_interface import IProductRepository
from app import db

from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel

class ProductRepository(IProductRepository):
    def __init__(self):
        super().__init__()

    def create_artisan_product(self, product_entity):
        """
        Saves a Product entity to the database.
        Converts the pure domain entity to a database model before saving.
        """
        
        # CONVERSION: Pure Domain Entity -> ORM Model
        product_db_model = ProductDBModel(
            product_id=product_entity.product_id,
            name=product_entity.name,
            description=product_entity.description,
            price=product_entity.price,
            stock=product_entity.stock,
            artisan_id=product_entity.artisan_id
        )
        
        print("Product DB Model: ", product_db_model)
        try:
            db.session.add(product_db_model)
            db.session.commit()
        except Exception as e:
            print(f"Error saving product: {e}")
            db.session.rollback()
        
        print("Product Entity after save: ", product_entity)
        return product_entity  # Retorna a entidade pura que foi salva