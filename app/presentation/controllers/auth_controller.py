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

# app/presentation/controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

# Import services and repository implementations for dependency injection
from app.application.services.user_registration_service import UserRegistrationService
from app.infrastructure.persistence.user_repository import UserRepository
from app.infrastructure.persistence.artisan_repository import ArtisanRepository

# Import DTOs for request and response formatting
from app.presentation.dtos.user_dtos import RegisterArtisanRequest, UserResponse

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# --- Manual Dependency Injection Setup ---
# Instantiate the concrete repository implementations
user_repository_instance = UserRepository()
artisan_repository_instance = ArtisanRepository()

# Instantiate the application service, injecting its dependencies
user_registration_service_instance = UserRegistrationService(
    user_repository=user_repository_instance,
    artisan_repository=artisan_repository_instance
)
# --- End of Manual Dependency Injection Setup ---

class AuthController:
    def __init__(self, user_registration_service: UserRegistrationService):
        self.user_registration_service = user_registration_service

    @auth_bp.route('/register/artisan', methods=['POST'])
    def register_artisan_route(self):
        """
        API endpoint for artisan registration.
        Handles POST requests to /api/register/artisan.
        """
        try:
            request_data = RegisterArtisanRequest(**request.json)
            
            user_entity = self.user_registration_service.register_artisan( # Chama o serviço via self
                request_data
            )
            
            return jsonify(UserResponse.from_domain_entity(user_entity).dict()), 201 
        
        except ValidationError as e:
            print(f"Validation Error: {e.errors()}")
            return jsonify({"error": "Invalid input data", "details": e.errors()}), 400
        
        except ValueError as e: 
            print(f"Business Logic Error: {e}")
            return jsonify({"error": str(e)}), 400
        
        except Exception as e: 
            print(f"Internal server error during artisan registration: {e}")
            return jsonify({"error": "Internal server error"}), 500

