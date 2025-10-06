from app.domain.repositories.buyer_repository_interface import IBuyerRepository
from app.extensions import SessionLocal
from app.infrastructure.persistence.models_db.buyer_db_model import BuyerDBModel

class BuyerRepository(IBuyerRepository):
    def __init__(self):
        super().__init__()

    def create(self, buyer_entity):
        """
        Saves an Buyer entity to the database.
        Converts the pure domain entity to a database model before saving.
        """
        # CONVERSION: Pure Domain Entity -> ORM Model
        buyer_db_model = BuyerDBModel(
            buyer_id=buyer_entity.buyer_id,
            full_name=buyer_entity.full_name,
            phone=buyer_entity.phone,
        )
        
        print("Buyer DB Model: ", buyer_db_model)
        session = SessionLocal()
        try:
            session.add(buyer_db_model)
            session.commit()
            # Update entity with generated ID if needed
            buyer_entity.buyer_id = buyer_db_model.buyer_id
        except Exception as e:
            print(f"Error saving buyer: {e}")
            session.rollback()
            raise
        finally:
            session.close()
        
        print("Buyer Entity after save: ", buyer_entity)
        return buyer_entity  # Retorna a entidade pura que foi salva