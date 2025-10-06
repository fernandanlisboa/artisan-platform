#open pointo to the API
"""
Propósito: Atuar como o ponto de entrada da API para o registro de artesãos.
Lógica:
Definir a rota POST /api/register/artisan.
Receber a requisição HTTP.
Validar o corpo da requisição usando RegisterArtisanRequest (isso captura erros de formato e campos obrigatórios, lançando ValidationError).
Instanciar ou obter os repositórios (UserRepositoryImpl, ArtisanRepositoryImpl).
Instanciar o serviço de aplicação (UserRegistrationService), passando os repositórios para ele (Injeção de Dependência manual).
Chamar o método register_artisan() do UserRegistrationService, passando os dados validados.
Capturar exceções de negócio lançadas pelo serviço (ex: ValueError para "Email already registered" ou "Store name already taken") e transformá-las em respostas HTTP 400 Bad Request (ou 409 Conflict se for mais específico).
Se o registro for bem-sucedido, pegar a entidade de usuário (User pura) retornada pelo serviço.
Converter a User entity para um UserResponse DTO.
Retornar uma resposta HTTP 201 Created com o corpo JSON contendo os dados do UserResponse.
Capturar quaisquer erros inesperados (Exception) e retornar 500 Internal Server Error.
"""
#TODO separar em dois controladores, um para artesão e outro para comprador
# app/presentation/controllers/auth_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

from app.application.services.user_registration_service import UserRegistrationService
from app.infrastructure.persistence.user_repository import UserRepository
from app.infrastructure.persistence.artisan_repository import ArtisanRepository
from app.infrastructure.persistence.buyer_repository import BuyerRepository
from app.infrastructure.persistence.address_repository import AddressRepository
from app.presentation.dtos.user_dtos import RegisterArtisanRequest, ArtisanRegistrationResponse, RegisterBuyerRequest, BuyerRegistrationResponse

# Configurar dependências
def get_registration_service():
    user_repo = UserRepository()
    artisan_repo = ArtisanRepository()
    buyer_repo = BuyerRepository()
    address_repo = AddressRepository()
    
    return UserRegistrationService(
        user_repository=user_repo,
        artisan_repository=artisan_repo,
        buyer_repository=buyer_repo,
        address_repository=address_repo
    )

class RegisterController:
    """Controller para operações de registro de usuários."""
    
    def __init__(self):
        self.router = APIRouter(
            prefix="/auth",
            tags=["Authentication"],
            responses={404: {"description": "Not found"}},
        )
        
        # Registrar rotas
        self.router.add_api_route(
            "/register/artisan",
            self.register_artisan,
            methods=["POST"],
            response_model=ArtisanRegistrationResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Register a new artisan",
            response_description="The created artisan user"
        )
        
        self.router.add_api_route(
            "/register/buyer",
            self.register_buyer,
            methods=["POST"],
            response_model=BuyerRegistrationResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Register a new buyer",
            response_description="The created buyer user"
        )

    async def register_artisan(
        self,
        request_data: RegisterArtisanRequest,
        service: UserRegistrationService = Depends(get_registration_service)
    ):
        """
        Register a new artisan with the following information:
        
        - **email**: Valid email address
        - **password**: Strong password (min 8 characters)
        - **store_name**: Name of the artisan's store
        - **phone**: Optional phone number
        - **bio**: Optional biography
        - **address**: Optional address information
        """
        try:
            return service.register_artisan(request_data=request_data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            print(f"Internal error during artisan registration: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    async def register_buyer(
        self,
        request_data: RegisterBuyerRequest,
        service: UserRegistrationService = Depends(get_registration_service)
    ):
        """Register a new buyer."""
        try:
            return service.register_buyer(request_data=request_data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            print(f"Internal error during buyer registration: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

# Instanciar o controller para exportar o router
register_controller = RegisterController()
register_router = register_controller.router
