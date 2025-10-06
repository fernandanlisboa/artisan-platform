from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from app.application.services.auth_service import AuthService
from app.infrastructure.persistence.user_repository import UserRepository
from app.presentation.dtos.auth_dtos import LoginRequest, LoginResponse

def get_auth_service():
    user_repo = UserRepository()
    return AuthService(user_repository=user_repo)

class AuthController:
    """Controller para operações de autenticação."""
    
    def __init__(self):
        self.router = APIRouter(
            prefix="/auth",
            tags=["Authentication"],
            responses={401: {"description": "Unauthorized"}}
        )
        
        # Registrar rotas
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            response_model=LoginResponse,
            status_code=status.HTTP_200_OK,
            summary="Authenticate user",
            description="Login with email and password"
        )
    
    async def login(
        self,
        login_data: LoginRequest,
        service: AuthService = Depends(get_auth_service)
    ):
        """Login endpoint para autenticação de usuários."""
        user = service.authenticate_user(
            email=login_data.email, 
            password=login_data.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Aqui você adicionaria a lógica para criar tokens JWT
        # ou outras informações de sessão
        
        return LoginResponse(
            user_id=user.user_id,
            email=user.email
        )


# Instanciar o controller para exportar o router
auth_controller = AuthController()
auth_router = auth_controller.router

