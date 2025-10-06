from app.domain.repositories.product_repository_interface import IProductRepository
from app.extensions import SessionLocal
from app.domain.models.product import ProductEntity
from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel

class ProductRepository(IProductRepository):
    def __init__(self):
        super().__init__()

    def create(self, product_entity):
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
            artisan_id=product_entity.artisan_id,
            status=product_entity.status,
            image_url=product_entity.image_url,
            category_id=product_entity.category_id,
        )
        
        print("Product DB Model: ", product_db_model)
        session = SessionLocal()
        try:
            session.add(product_db_model)
            session.commit()
            product_entity = ProductEntity.from_db_model(product_db_model)
        except Exception as e:
            print(f"Error saving product: {e}")
            session.rollback()
            raise
        finally:
            session.close()
        print("Product Entity after save: ", product_entity)
        return product_entity  
    
    def get_product_by_id(self, product_id):
        """
        Retrieves a Product entity by its ID.
        Converts the ORM model to a pure domain entity.
        """
        session = SessionLocal()
        try:
            product_db_model = session.get(ProductDBModel, product_id)
            if product_db_model:
                return ProductEntity.from_db_model(product_db_model)
            return None
        finally:
            session.close()
        
    def get_artisan_product_by_name(self, artisan_id, product_name):
        """
        Retrieves a Product entity by its name and artisan ID.
        Converts the ORM model to a pure domain entity.
        """
        session = SessionLocal()
        try:
            product_db_model = session.query(ProductDBModel).filter_by(
                artisan_id=artisan_id, name=product_name).first()
            if product_db_model:
                return ProductEntity.from_db_model(product_db_model)
            return None
        finally:
            session.close()
    
    def find_by_artisan_id(self, artisan_id: str):
        """
        Finds all products associated with a specific artisan ID.
        Converts ORM models to pure domain entities.
        """
        session = SessionLocal()
        try:
            product_db_models = session.query(ProductDBModel).filter_by(
                artisan_id=artisan_id).all()
            if product_db_models:
                return [ProductEntity.from_db_model(product) 
                        for product in product_db_models]
            return []
        except Exception as e:
            print(f"Error retrieving products for artisan {artisan_id}: {e}")
            return []
        finally:
            session.close()
        