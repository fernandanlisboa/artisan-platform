from abc import ABC, abstractmethod
from app.domain.models.user import UserEntity
from typing import Optional

#interface
class IUserRepository(ABC):
    """
    Interface (Abstract Base Class) for User data access operations.
    Defines the contract for interacting with the 'users' table.
    """
    @abstractmethod
    def create(self, user_entity: UserEntity) -> UserEntity:
        """
        Save a user to the repository.
        
        :param user: UserEntity instance to be saved.
        :return: The saved UserEntity instance.
        """
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Retrieve a user by email.
        
        :param email: Email of the user to retrieve.
        :return: UserEntity instance if found, None otherwise.
        """
        pass        
