from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime, timezone
class UserEntity(ABC):
    def __init__(self, email, hashed_password, status, user_id: Optional[str] = None, address_id: Optional[str] = None, registration_date: Optional[datetime] = None):
        self.user_id = user_id
        self.email = email
        self.hashed_password = hashed_password
        self.status = status
        self.address_id = address_id 
        if registration_date is None:
            self.registration_date = datetime.now(timezone.utc)

    @classmethod
    def from_db_model(cls, db_model):
        return cls(
            user_id=db_model.user_id,
            email=db_model.email,
            hashed_password=db_model.hashed_password,
            status=db_model.status,
            address_id=db_model.address_id
        )

    def __repr__(self):
        return f"UserEntity(user_id={self.user_id}, email={self.email}, status={self.status}, address_id={self.address_id})"