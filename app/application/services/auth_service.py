from typing import Optional
from app.common.password_utils import verify_password
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.models.user import UserEntity as User


class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticates a user with email and password.
        
        Args:
            email: The user's email
            password: The plain text password to check
        
        Returns:
            User: The authenticated user or None if authentication fails
        """
        if user := self.user_repository.get_by_email(email):
                # Check if the provided password matches the stored Argon2 hash
            return user if verify_password(password, user.hashed_password) else None
        else:
            return None
