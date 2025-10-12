from typing import Optional
from app.common.password_utils import verify_password
from app.common.jwt_utils import JWTManager
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.models.user import UserEntity as User
from app.presentation.dtos.auth_dtos import LoginRequest, LoginResponse
from app.common.config import config_by_name
import os


class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        
        # Obter configuração atual
        config_name = os.getenv('API_ENV', 'development')
        self.config = config_by_name[config_name]
    
    def _generate_jwt_tokens(self, user: User) -> tuple[str, str]:
        """
        Gera tokens JWT de acesso e refresh para um usuário.
        
        Args:
            user: Entidade do usuário
            
        Returns:
            tuple: (access_token, refresh_token)
        """
        # Gerar token de acesso
        access_token = JWTManager.generate_access_token(
            user_id=str(user.user_id),
            email=user.email,
            # Você pode adicionar claims extras aqui se necessário
            # role=user.role,
            # permissions=user.permissions
        )
        
        # Gerar token de refresh
        refresh_token = JWTManager.generate_refresh_token(
            user_id=str(user.user_id),
            email=user.email
        )
        
        return access_token, refresh_token

    def authenticate_user(self, login_request: LoginRequest) -> Optional[LoginResponse]:
        """
        Authenticates a user with email and password.
        
        Args:
            login_request: Dados de login do usuário
        
        Returns:
            LoginResponse: Resposta de login com tokens JWT ou None se falhar
            
        Raises:
            ValueError: Se o usuário não for encontrado ou senha inválida
        """
        email = login_request.email
        password = login_request.password
        
        # Buscar usuário pelo email
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        
        # Verificar senha
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid password")
        
        # Gerar tokens JWT
        access_token, refresh_token = self._generate_jwt_tokens(user)

        return LoginResponse(
            user_id=str(user.user_id),
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=self.config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60  # converter para segundos
        )
