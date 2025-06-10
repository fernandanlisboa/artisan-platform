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
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

# --- IMPORTAÇÕES PARA FLASK-RESTX ---
from flask_restx import Namespace, Resource, fields # Importa Namespace, Resource e fields
# --- FIM DAS IMPORTAÇÕES ---

# Import services and repository implementations for dependency injection
from app.application.services.user_registration_service import UserRegistrationService
from app.infrastructure.persistence.user_repository import UserRepository
from app.infrastructure.persistence.artisan_repository import ArtisanRepository
from app.infrastructure.persistence.buyer_repository import BuyerRepository # Placeholder, se você tiver um repositório de comprador
from app.infrastructure.persistence.address_repository import AddressRepository

# Import DTOs for request and response formatting
from app.presentation.dtos.user_dtos import RegisterArtisanRequest, ArtisanRegistrationResponse, RegisterBuyerRequest, BuyerRegistrationResponse

# --- CRIAÇÃO DO NAMESPACE (Ele agrupa rotas e documentação) ---
auth_ns = Namespace('auth', description='Authentication related operations') 
# --- Fim da Criação ---


address_request_model = auth_ns.model('RegisterAddressRequest', {
    'street': fields.String(required=True, description='Street name', example='Rua das Flores', max_length=255),
    'number': fields.String(description='House/building number', required=False, max_length=20),
    'complement': fields.String(description='Complementary address info', required=False, max_length=100),
    'neighborhood': fields.String(required=True, description='Neighborhood', example='Centro', max_length=100),
    'city': fields.String(required=True, description='City', example='Salvador', max_length=100),
    'state': fields.String(required=True, description='State abbreviation (e.g., BA)', max_length=2),
    'zip_code': fields.String(required=True, description='Postal code (CEP)', example='40000-000', max_length=10),
    'country': fields.String(description='Country', required=False, default='Brasil', max_length=100),
})

# --- DEFINIÇÃO DO MODELO DE REQUISIÇÃO DE ARTESÃO PARA FLASK-RESTX - AGORA COM ENDEREÇO ANINHADO ---
artisan_registration_request_model = auth_ns.model('RegisterArtisanRequest', {
    'email': fields.String(required=True, description='User email', example='artisan@example.com'),
    'password': fields.String(required=True, description='User password', min_length=8),
    'store_name': fields.String(required=True, description='Name of the artisan\'s store', max_length=255),
    'phone': fields.String(description='Artisan\'s phone number', required=False),
    'bio': fields.String(description='Artisan\'s biography', required=False),
    
    # --- NOVO: Campo de Endereço Aninhado no modelo Flask-RESTx ---
    'address': fields.Nested(address_request_model, description='Optional primary address details for the artisan', required=False),
})

address_response_model = auth_ns.model('AddressResponseOutput', { # Nome diferente para evitar conflito se você tiver um 'AddressResponse' de input
    'address_id': fields.String(
        required=True,
        description='ID único do endereço.',
        example="a1b2c3d4-e5f6-7890-1234-567890abcdef"
    ),
    'street': fields.String(
        required=True,
        description='Nome da rua.',
        example="Rua das Palmeiras"
    ),
    'number': fields.String(
        required=False, # Opcional
        description='Número da residência/comércio.',
        example="123A"
    ),
    'complement': fields.String(
        required=False, # Opcional
        description='Complemento do endereço (ex: Apto, Bloco).',
        example="Apto 4B"
    ),
    'neighborhood': fields.String(
        required=True,
        description='Bairro.',
        example="Centro"
    ),
    'city': fields.String(
        required=True,
        description='Cidade.',
        example="Cidade das Artes"
    ),
    'state': fields.String(
        required=True,
        description='Estado (sigla).',
        example="BA"
    ),
    'zip_code': fields.String(
        required=True,
        description='CEP.',
        example="40000-000"
    ),
    'country': fields.String(
        required=True,
        description='País.',
        default='Brasil',
        example="Brasil"
    )
})

# 2. Modelo Principal para a Resposta de Registro de Artesão
# Este é o modelo que você usará no @auth_ns.marshal_with()
artisan_registration_response_model = auth_ns.model('ArtisanRegistrationResponseOutput', { # Nome diferente para output
    'user_id': fields.String(
        required=True,
        description='ID único do usuário (que também é o ID do artesão).',
        example="u1b2c3d4-e5f6-7890-1234-567890abcdef"
    ),
    'email': fields.String(
        required=True,
        description='Email de login do artesão.',
        example="artesao@email.com"
    ),
    'store_name': fields.String( # "nome do artesão"
        required=True,
        description='Nome da loja ou ateliê do artesão.',
        example="Ateliê Mãos de Ouro"
    ),
    'phone': fields.String(
        required=False, # Opcional
        description='Telefone de contato do artesão.',
        example="71999998888"
    ),
    'bio': fields.String(
        required=False, # Opcional
        description='Biografia ou descrição do trabalho do artesão.',
        example="Crio peças únicas em cerâmica, inspiradas na natureza local."
    ),
    'registration_date': fields.DateTime(
        required=True,
        description='Data e hora em que o usuário foi registrado.',
        dt_format='iso8601' # Formato padrão, mas pode ser especificado
    ),
    'status': fields.String(
        required=True,
        description='Status atual da conta do usuário (ex: active, pending_verification).',
        example="active"
    ),
    'role': fields.String(
        required=True,
        description='Papel do usuário no sistema.',
        example='artisan', # Default para o contexto de registro de artesão
        default='artisan'
    ),
    'address': fields.Nested( # Campo para o endereço aninhado
        address_response_model, # Usa o modelo de endereço definido acima
        required=False,         # O endereço como um todo é opcional no registro
        description='Endereço principal associado ao artesão.',
        skip_none=True          # Se o objeto de endereço for None, a chave 'address' será omitida da resposta JSON
    )
})
                                    
# --- Fim das Definições de Modelos ---
# --- Setup de Injeção de Dependência (manual, no módulo) ---
user_repository_instance = UserRepository() 
artisan_repository_instance = ArtisanRepository() 
address_repository_instance = AddressRepository()
buyer_repository_instance = BuyerRepository()

user_registration_service_instance = UserRegistrationService(
    user_repository=user_repository_instance,
    artisan_repository=artisan_repository_instance,
    address_repository=address_repository_instance,
    buyer_repository=buyer_repository_instance 
)
# -
# --- CONTROLADOR COMO UM RECURSO FLASK-RESTX ---
@auth_ns.route('/register/artisan') # A rota é definida no namespace
class ArtisanRegistrationResource(Resource): # HERDA DE flask_restx.Resource
    """Resource for artisan registration."""
    
    # Injeta o serviço de aplicação no recurso (como atributo de classe)
    user_registration_service = user_registration_service_instance

    @auth_ns.expect(artisan_registration_request_model, validate=True) # Validação de entrada Pydantic/Swagger
    @auth_ns.marshal_with(artisan_registration_response_model, code=201) # Formatação de saída e documentação
    @auth_ns.doc(description='Register a new artisan user.')
    def post(self): # O método HTTP (POST) é o nome da função. 'self' é gerenciado pelo Flask-RESTx.
        """Registers a new artisan."""
        try:
            # auth_ns.payload contém os dados JSON já parseados e validados pelo @auth_ns.expect
            request_data = RegisterArtisanRequest(**auth_ns.payload)
            
            # Chama o serviço de aplicação (acessado via self.user_registration_service)
            created_user = self.user_registration_service.register_artisan(
                request_data=request_data
            )
            
            # Flask-RESTx cuida do jsonify e status code via @auth_ns.marshal_with
            return created_user, 201 # Retorna a entidade pura, Flask-RESTx a formata
        
        except ValidationError as e:
            # Embora @auth_ns.expect já lide com isso, você pode capturar se precisar de mais controle
            auth_ns.abort(400, "Invalid input data", details=e.errors())
        
        except ValueError as e: # Captura erros de lógica de negócio do serviço
            auth_ns.abort(400, str(e)) 
        
        except Exception as e: # Captura outros erros inesperados
            print(f"Internal server error during artisan registration: {e}") 
            auth_ns.abort(500, "Internal server error")



# --- DEFINIÇÃO DO MODELO DE REQUISIÇÃO DE COMPRADOR PARA FLASK-RESTX ---
buyer_registration_request_model = auth_ns.model('RegisterBuyerRequest', {
    'email': fields.String(required=True, description='User email', example='buyer@example.com'),
    'password': fields.String(required=True, description='User password', min_length=8),
    'full_name': fields.String(required=True, description='Buyer\'s full name', max_length=255, example='John Doe'),
    'phone': fields.String(description='Buyer\'s phone number', required=False, example='5571999998888'),
    
    # Campo de Endereço Aninhado (reusa o mesmo modelo de endereço)
    'address': fields.Nested(address_request_model, description='Primary address details for the buyer', required=False),
})

# Modelo de resposta para registro de comprador
buyer_registration_response_model = auth_ns.model('BuyerRegistrationResponseOutput', {
    'user_id': fields.String(
        required=True,
        description='Unique ID of the user (also the buyer ID)',
        example="b1b2c3d4-e5f6-7890-1234-567890abcdef"
    ),
    'email': fields.String(
        required=True,
        description='Login email of the buyer',
        example="buyer@example.com"
    ),
    'full_name': fields.String(
        required=True,
        description='Buyer\'s full name',
        example="John Doe"
    ),
    'phone': fields.String(
        required=False,
        description='Buyer\'s contact phone',
        example="71999998888"
    ),
    'registration_date': fields.DateTime(
        required=True,
        description='Date and time when the user was registered',
        dt_format='iso8601'
    ),
    'status': fields.String(
        required=True,
        description='Current status of the user account',
        example="active"
    ),
    'role': fields.String(
        required=True,
        description='User role in the system',
        example='buyer',
        default='buyer'
    ),
    'address': fields.Nested(
        address_response_model,
        required=False,
        description='Primary address associated with the buyer',
        skip_none=True
    )
})
#FIX: time out
@auth_ns.route('/register/buyer')
class BuyerRegistrationResource(Resource):
    """Resource for buyer registration."""
    
    # Injeta o serviço de aplicação no recurso
    user_registration_service = user_registration_service_instance

    @auth_ns.expect(buyer_registration_request_model, validate=True)
    @auth_ns.marshal_with(buyer_registration_response_model, code=201)
    @auth_ns.doc(description='Register a new buyer user.')
    def post(self):
        """Registers a new buyer."""
        try:
            # Converte os dados da requisição para o DTO
            request_data = RegisterBuyerRequest(**auth_ns.payload)
            
            # Chama o serviço de aplicação
            created_user = self.user_registration_service.register_buyer(
                request_data=request_data
            )
            
            # Retorna a resposta formatada
            return created_user, 201
        
        except ValidationError as e:
            auth_ns.abort(400, "Invalid input data", details=e.errors())
        
        except ValueError as e:
            auth_ns.abort(400, str(e))
        
        except Exception as e:
            print(f"Internal server error during buyer registration: {e}")
            auth_ns.abort(500, "Internal server error")
