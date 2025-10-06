from app.domain.repositories.user_repository_interface import IUserRepository
from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
from app.extensions import SessionLocal
from app.domain.models.user import UserEntity
from datetime import datetime, timezone

class UserRepository(IUserRepository):
    def __init__(self):
        super().__init__()

    def create(self, user_entity) -> UserEntity:
        """Saves a User entity to the database by converting it to UserDBModel."""
        # CONVERSION: Pure Domain Entity -> ORM Model
        user_db_model = UserDBModel(
            email=user_entity.email,
            hashed_password=user_entity.hashed_password, 
            status=user_entity.status,
            registration_date=datetime.now(timezone.utc),
            address_id=user_entity.address_id
        )
        print("User DB Model: ", user_db_model)
        
        # Create a new session for this operation
        session = SessionLocal()
        try:
            session.add(user_db_model)
            session.commit()
            
            # Update domain entity with generated values
            user_entity.user_id = user_db_model.user_id
            user_entity.registration_date = user_db_model.registration_date
            
            print("User Entity after save: ", user_entity)
            return user_entity
        except Exception as e:
            print(f"Error saving user: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_by_email(self, email: str) -> UserEntity:
        """Retrieves a User entity by email."""
        #TODO: check also if the user is active
        session = SessionLocal()
        try:
            user_db_model = session.query(UserDBModel).filter_by(email=email).first()
            if user_db_model:
                user_entity = UserEntity.from_db_model(user_db_model)
                return user_entity
            return None
        finally:
            session.close()
