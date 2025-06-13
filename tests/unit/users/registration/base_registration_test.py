import pytest
from unittest.mock import Mock
from tests.unit.users.base_test import BaseUserTest
from app.application.services.user_registration_service import UserRegistrationService
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.repositories.buyer_repository_interface import IBuyerRepository
from app.domain.repositories.address_repository_interface import IAddressRepository
from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app.presentation.dtos.user_dtos import RegisterAddressRequest
from tests.unit.mocks.factories import MockFactory

mock_factory = MockFactory()
class BaseRegistrationTest(BaseUserTest):
    """Classe base para testes de registro de usuários."""

    @pytest.fixture
    def mock_repositories(self):
        """Configura repositórios mock para todos os testes."""
        return {
            'user_repo': Mock(spec=IUserRepository),
            'artisan_repo': Mock(spec=IArtisanRepository),
            'address_repo': Mock(spec=IAddressRepository),
            'buyer_repo': Mock(spec=IBuyerRepository)
        }
    
    @pytest.fixture
    def service(self, mock_repositories):
        """Cria o serviço com repositórios mockados."""
        return UserRegistrationService(
            user_repository=mock_repositories['user_repo'],
            artisan_repository=mock_repositories['artisan_repo'],
            address_repository=mock_repositories['address_repo'],
            buyer_repository=mock_repositories['buyer_repo']
        )
    
    @pytest.fixture
    def valid_address_request(self):
        """Cria um objeto de requisição de endereço válido."""
        address = mock_factory.address.create()
        return {
            'street': address.street,
            'number': address.number,
            'complement': address.complement,
            'neighborhood': address.neighborhood,
            'city': address.city,
            'state': address.state,
            'zip_code': address.zip_code,
            'country': address.country
        }
    
    @pytest.fixture
    def valid_user_request(self, valid_address_request):
        """Cria uma requisição válida de usuário."""
        user = mock_factory.user.create()
        return {
            'email': user.email,
            'password': "ValidPassword123!",
            'address': valid_address_request
        }
    
    @pytest.fixture
    def mock_entities(self, test_ids):
        """Usa a MockFactory para criar entidades de teste."""
        return {
            'user': mock_factory.user.create(user_id=test_ids['user_id']),
            'address': mock_factory.address.create(address_id=test_ids['address_id']),
            'buyer': mock_factory.buyer.create(buyer_id=test_ids['user_id']),
            'artisan': mock_factory.artisan.create(artisan_id=test_ids['user_id'])
        }
    
    def _setup_successful_registration(self, mock_repositories, mock_entities, user_type, request=None):
        """Configura mocks para um registro bem-sucedido."""
        # Use objetos concretos em vez de mocks diretos
        
        if hasattr(request, 'email'):
            # 2. Atualizar o email no mock_entities['user'] para corresponder à requisição
            mock_entities['user'].email = request.email
        
        mock_repositories['user_repo'].get_by_email.return_value = None
        mock_repositories['user_repo'].create.return_value = mock_entities['user']
        
        # CORREÇÃO AQUI: Configurar o comportamento do método, não chamar o método
        mock_repositories['address_repo'].get_by_attributes.return_value = None
        mock_repositories['address_repo'].get_by_id.return_value = mock_entities['address']
        mock_repositories['address_repo'].create.return_value = mock_entities['address']
        
        mock_repositories[f'{user_type}_repo'].create.return_value = mock_entities[user_type]
    
    def _assert_successful_registration(self, result, request, mock_repositories, test_ids, user_type):
        """Verifica asserções comuns para registro bem-sucedido."""
        assert result is not None
        assert result.user_id == test_ids['user_id']
        assert result.email == request.email
        
        # Verifica chamadas aos repositórios
        mock_repositories['user_repo'].get_by_email.assert_called_once_with(request.email)
        mock_repositories['address_repo'].create.assert_called_once()
        mock_repositories['user_repo'].create.assert_called_once()
        
        # Verifica apenas que o método foi chamado, sem verificar os argumentos exatos
        mock_repositories[f'{user_type}_repo'].create.assert_called_once()
        
        # Opcionalmente, verifica que o argumento é uma entidade do tipo correto
        args, kwargs = mock_repositories[f'{user_type}_repo'].create.call_args
        if args:  # Se os argumentos foram passados como args posicionais
            if user_type == 'artisan':
                from app.domain.models.artisan import ArtisanEntity
                assert isinstance(args[0], ArtisanEntity)
                assert args[0].artisan_id == test_ids['user_id']
            else:  # buyer
                from app.domain.models.buyer import BuyerEntity
                assert isinstance(args[0], BuyerEntity)
                assert args[0].buyer_id == test_ids['user_id']
    
    def _test_duplicate_email(self, service, mock_repositories, request, mock_entities):
        """Testa validação de email duplicado."""
        # Arrange
        mock_repositories['user_repo'].get_by_email.return_value = mock_entities['user']
        
        # Act & Assert
        with pytest.raises(ValueError):
            self._registration_method(service, request)
        
        # Verify
        mock_repositories['user_repo'].get_by_email.assert_called_once()
        mock_repositories['address_repo'].create.assert_not_called()
        mock_repositories['user_repo'].create.assert_not_called()