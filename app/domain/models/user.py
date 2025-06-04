from abc import ABC, abstractmethod

class UserEntity(ABC):
    def __init__(self, user_id, email, password, status, address_id=None):
        self.user_id = user_id
        self.email = email
        self.password = password # Aqui seria a senha limpa, antes do hash
        self.status = status
        self.address_id = address_id  # Novo campo
        
        # Hash the password during entity creation
        # self.password_hash = self._hash_password(password)