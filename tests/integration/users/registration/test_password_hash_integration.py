import pytest
import uuid
from app.application.services.user_registration_service import UserRegistrationService
from app.common.password_utils import verify_password
from app.infrastructure.persistence.address_repository import AddressRepository
from app.infrastructure.persistence.artisan_repository import ArtisanRepository
from app.infrastructure.persistence.buyer_repository import BuyerRepository
from app.infrastructure.persistence.user_repository import UserRepository
from app.presentation.dtos.user_dtos import RegisterBuyerRequest

@pytest.fixture
def repositories(app):
    """Inicializa os repositórios reais, não mocks."""
    with app.app_context():
        return {
            'user_repo': UserRepository(),
            'buyer_repo': BuyerRepository(),
            'address_repo': AddressRepository(),
            'artisan_repo': ArtisanRepository()
        }
@pytest.fixture
def service(repositories):
    """Cria o serviço com repositórios reais."""
    return UserRegistrationService(
        user_repository=repositories['user_repo'],
        buyer_repository=repositories['buyer_repo'],
        address_repository=repositories['address_repo'],
        artisan_repository=repositories['artisan_repo']
    )


class TestPasswordHashIntegration:
    """Testes de integração específicos para a funcionalidade de hash de senha.
    """
    
    @pytest.fixture
    def valid_registration_data(self):
        """Cria dados válidos para registro."""
        unique_email = f"pwd_test_{uuid.uuid4().hex[:8]}@example.com"
        return {
            "email": unique_email,
            "password": "StrongP@ssw0rd",
            "full_name": "Teste de Hash",
            "phone": "(11) 98765-4321",
            "address": {
                "street": "Rua do Teste",
                "number": "123",
                "neighborhood": "Bairro Teste",
                "city": "Cidade Teste",
                "state": "SP",
                "zip_code": "12345-678",
                "country": "Brasil"
            }
        }
 
    def test_buyer_hashed_password_persistence(self, client, service, valid_registration_data, app):
        """Verifica se a senha do comprador é hasheada antes de ser persistida."""
        with app.app_context():
            # Arrange
            request_data = RegisterBuyerRequest(**valid_registration_data)
            plain_password = request_data.password
            
            # Act
            result = service.register_buyer(request_data)
            
            # Assert
            from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
            saved_user = UserDBModel.query.get(result.user_id)
            
            # Verificar que a senha salva é um hash, não texto plano
            assert saved_user.hashed_password != plain_password
            assert saved_user.hashed_password.startswith("$argon2")
            
            # Verificar que a senha pode ser validada corretamente
            assert verify_password(plain_password, saved_user.hashed_password)