from app.domain.repositories.product_repository_interface import IProductRepository
from app import db
from app.domain.models.product import ProductEntity
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
        return product_entity  
    
    def get_product_by_id(self, product_id):
        """
        Retrieves a Product entity by its ID.
        Converts the ORM model to a pure domain entity.
        """
        product_db_model = ProductDBModel.query.get(product_id)
        
        if product_db_model:
            return ProductEntity.from_db_model(product_db_model)
        return None
        
    def get_artisan_product_by_name(self, artisan_id, product_name):
        """
        Retrieves a Product entity by its name and artisan ID.
        Converts the ORM model to a pure domain entity.
        """
        product_db_model = ProductDBModel.query.filter_by(
            artisan_id=artisan_id, name=product_name).first()
        
        if product_db_model:
            return ProductEntity.from_db_model(product_db_model)
        return None