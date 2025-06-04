from app.domain.repositories.user_repository_interface import IUserRepository
from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
from app import db

from datetime import datetime

class UserRepository(IUserRepository):
    def __init__(self):
        super().__init__()

    def save(self, user_entity):
        """Saves a User entity to the database by converting it to UserDBModel."""
        # CONVERSION: Pure Domain Entity -> ORM Model
        user_db_model = UserDBModel(
            user_id=user_entity.user_id,
            email=user_entity.email,
            password_hash=user_entity.password, 
            status=user_entity.status,
            registration_date=datetime.utcnow(),
            address_id=user_entity.address_id  # Added address_id
        )
        
        # Persistence
        existing_user = db.session.query(UserDBModel).get(user_db_model.user_id)
        if existing_user:
            db.session.merge(user_db_model) 
        else:
            db.session.add(user_db_model) 
        
        db.session.commit()
        return user_entity # Returns the pure entity that was saved