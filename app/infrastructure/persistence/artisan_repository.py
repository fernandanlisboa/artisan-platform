from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app.extensions import SessionLocal
from app.domain.models.artisan import ArtisanEntity
from app.infrastructure.persistence.models_db.artisan_db_model import ArtisanDBModel

class ArtisanRepository(IArtisanRepository):
    def __init__(self):
        super().__init__()

    def create(self, artisan_entity):
        """
        Saves an Artisan entity to the database.
        Converts the pure domain entity to a database model before saving.
        """
        # CONVERSION: Pure Domain Entity -> ORM Model
        artisan_db_model = ArtisanDBModel(
            artisan_id=artisan_entity.artisan_id,
            store_name=artisan_entity.store_name,
            phone=artisan_entity.phone,
            bio=artisan_entity.bio,
        )
        
        print("Artisan DB Model: ", artisan_db_model)
        session = SessionLocal()
        try:
            session.add(artisan_db_model)
            session.commit()
            # Update entity with generated ID if needed
            artisan_entity.artisan_id = artisan_db_model.artisan_id
        except Exception as e:
            print(f"Error saving artisan: {e}")
            session.rollback()
            raise
        finally:
            session.close()
        
        print("Artisan Entity after save: ", artisan_entity)
        return artisan_entity # Retorna a entidade pura que foi salva
    
    def get_artisan_by_id(self, artisan_id):
        """
        Retrieves an Artisan entity by its ID.
        Converts the ORM model to a pure domain entity.
        """
        session = SessionLocal()
        try:
            artisan_db_model = session.get(ArtisanDBModel, artisan_id)
            
            if artisan_db_model:
                return ArtisanEntity.from_db_model(artisan_db_model)
            return None
        finally:
            session.close()