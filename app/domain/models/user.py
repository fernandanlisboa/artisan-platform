from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
class UserEntity(ABC):
    def __init__(self, email, password, status, user_id: Optional[str] = None, address_id: Optional[str] = None, registration_date: Optional[datetime] = None):
        self.user_id = user_id
        self.email = email
        self.password = password # Aqui seria a senha limpa, antes do hash
        self.status = status
        self.address_id = address_id 
        if registration_date is not None:
            self.registration_date = datetime.utcnow()
        # Hash the password during entity creation
        # self.password_hash = self._hash_password(password)
        
    def __repr__(self):
        return f"UserEntity(user_id={self.user_id}, email={self.email}, status={self.status}, address_id={self.address_id})"