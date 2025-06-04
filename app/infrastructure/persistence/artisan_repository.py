from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app import db

from app.infrastructure.persistence.models_db.artisan_db_model import ArtisanDBModel

class ArtisanRepository(IArtisanRepository):
    def __init__(self):
        super().__init__()

    def save(self, artisan_entity):
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
        
        # Persistence
        existing_user = db.session.query(ArtisanDBModel).get(artisan_db_model.artisan_id)
        if existing_user:
            db.session.merge(artisan_db_model) 
        else:
            db.session.add(artisan_db_model) 
        
        db.session.commit()
        return artisan_entity # Returns the pure entity that was saved