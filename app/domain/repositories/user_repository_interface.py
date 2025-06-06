from abc import ABC, abstractmethod
from app.domain.models.user import UserEntity

#interface
class IUserRepository(ABC):
    """
    Interface (Abstract Base Class) for User data access operations.
    Defines the contract for interacting with the 'users' table.
    """
    @abstractmethod
    def save(self, user_entity: UserEntity) -> UserEntity:
        """
        Save a user to the repository.
        
        :param user: UserEntity instance to be saved.
        :return: The saved UserEntity instance.
        """
        pass
        