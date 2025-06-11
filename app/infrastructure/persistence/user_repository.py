from app.domain.repositories.user_repository_interface import IUserRepository
from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
from app import db
from app.domain.models.user import UserEntity
from datetime import datetime

class UserRepository(IUserRepository):
    def __init__(self):
        super().__init__()

    def save(self, user_entity) -> UserEntity:
        """Saves a User entity to the database by converting it to UserDBModel."""
        # CONVERSION: Pure Domain Entity -> ORM Model
        user_db_model = UserDBModel(
            email=user_entity.email,
            password_hash=user_entity.password, 
            status=user_entity.status,
            # registration_date=datetime.utcnow,
            address_id=user_entity.address_id  # Added address_id
        )
        print("User DB Model: ", user_db_model)
        try:
            db.session.add(user_db_model)
            db.session.commit()
        except Exception as e:
            print(f"Error saving user: {e}")
            db.session.rollback()
            raise
        print("User DB Model after commit: ", user_db_model)
        user_entity.user_id = user_db_model.user_id  # Atualiza o ID da entidade pura com o ID gerado pelo banco
        print("User Entity after save: ", user_entity)
        return user_entity # Retorna a entidade pura que foi salva
    
    def get_by_email(self, email: str) -> UserEntity:
        """Retrieves a User entity by email."""
        #TODO: check also if the user is active
        user_db_model = UserDBModel.query.filter_by(email=email).first()
        if user_db_model:
            user_entity = UserEntity.from_db_model(user_db_model)
            return user_entity
        
        return None
