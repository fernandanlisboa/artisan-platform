from typing import Optional

class ArtisanEntity():
    """
    Represents an artisan user in the system.
    Inherits from UserEntity to include common user attributes.
    """
    
    def __init__(self, artisan_id: str, store_name: str, phone: str = None, bio: str = None): # type: ignore
        self.artisan_id = artisan_id
        self.phone = phone
        self.store_name = store_name
        self.bio = bio
        
    @classmethod
    def from_db_model(cls, db_model):
        """
        Converts a database model to a pure domain entity.
        This is useful for converting ORM models to domain entities.
        """
        return cls(
            artisan_id=db_model.artisan_id,
            store_name=db_model.store_name,
            phone=db_model.phone,
            bio=db_model.bio
        )

    def __repr__(self):
        return f"ArtisanEntity(artisan_id={self.artisan_id}, store_name={self.store_name}, phone={self.phone}, bio={self.bio})"
    