from app.domain.repositories.buyer_repository_interface import IBuyerRepository
from app import db

from app.infrastructure.persistence.models_db.buyer_db_model import BuyerDBModel

class BuyerRepository(IBuyerRepository):
    def __init__(self):
        super().__init__()

    def save(self, buyer_entity):
        """
        Saves an Buyer entity to the database.
        Converts the pure domain entity to a database model before saving.
        """
        # CONVERSION: Pure Domain Entity -> ORM Model
        buyer_db_model = BuyerDBModel(
            artisan_id=buyer_entity.buyer_id,
            full_name=buyer_entity.full_name,
            address=buyer_entity.address,
            phone=buyer_entity.phone,
        )
        
        print("Buyer DB Model: ", buyer_db_model)
        try:
            db.session.add(buyer_db_model)
            db.session.commit()
        except Exception as e:
            print(f"Error saving buyer: {e}")
            db.session.rollback()
        
        print("Buyer Entity after save: ", buyer_entity)
        return buyer_entity # Retorna a entidade pura que foi salva