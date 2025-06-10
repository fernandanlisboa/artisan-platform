import pytest
from unittest.mock import Mock
import uuid
import random
from app.application.services.user_registration_service import UserRegistrationService
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.repositories.buyer_repository_interface import IBuyerRepository
from app.domain.repositories.address_repository_interface import IAddressRepository
from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from tests.unit.mock_data import MockFactory, fake

from app.presentation.dtos.user_dtos import RegisterAddressRequest

class BaseUserRegistrationTest:
    """Classe base para testes de registro de usuários (artesão/comprador)"""
    
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
    def test_ids(self):
        """Gera IDs consistentes para uso nos testes."""
        return {
            'user_id': str(uuid.uuid4()),
            'address_id': str(uuid.uuid4())
        }
    
    @pytest.fixture
    def valid_address_request(self):
        """Cria um objeto de requisição de endereço válido."""
        return RegisterAddressRequest(
            street=fake.street_name(),
            number=fake.building_number(),
            complement=fake.secondary_address(),
            neighborhood=fake.city_suffix(),
            city=fake.city(),
            state=fake.state_abbr(),
            zip_code=fake.postcode(),
            country=fake.country()
        )

    def _generate_valid_phone(self, max_length=20):
        """Gera um número de telefone válido com comprimento máximo especificado."""
        formats = [
            '+## (##) ####-####',
            '(##) ####-####',
            '##-####-####',
            '+##########'
        ]
        
        format_template = random.choice(formats)
        return ''.join([str(fake.random_digit()) if c == '#' else c for c in format_template])
    
    def _setup_basic_mocks(self, mock_repositories, mock_entities, email_exists=False, address_exists=False):
        """Configura mocks básicos com parâmetros flexíveis."""
        mock_repositories['user_repo'].get_by_email.return_value = mock_entities['user'] if email_exists else None
        mock_repositories['address_repo'].get_by_attributes.return_value = mock_entities['address'] if address_exists else None
        
        # Se email não existe, configurar as chamadas de save
        if not email_exists:
            mock_repositories['address_repo'].save.return_value = mock_entities['address']
            mock_repositories['user_repo'].save.return_value = mock_entities['user']
    
    def _assert_common_validations(self, service, user_request, mock_repositories, error_message):
        """Realiza asserções comuns para validações de erro."""
        with pytest.raises(ValueError) as excinfo:
            # O método específico será chamado pela classe filha
            self._registration_method(service, user_request)
        
        assert error_message in str(excinfo.value)
        mock_repositories['user_repo'].save.assert_not_called()
        mock_repositories['buyer_repo'].save.assert_not_called()
        mock_repositories['artisan_repo'].save.assert_not_called()
    
    def _test_password_validations(self, service, mock_repositories, create_request_method):
        """Teste parametrizado para validações de senha."""
        mock_repositories['user_repo'].get_by_email.return_value = None
        
        test_cases = [
            {"password": "short", "expected": "8 characters"},
            {"password": "nouppercase123$", "expected": "uppercase"},
            {"password": "NOLOWERCASE123$", "expected": "lowercase"},
            {"password": "NoNumbers$", "expected": "number"},
            {"password": "NoSpecialChars123", "expected": "special character"}
        ]
        
        for case in test_cases:
            request = create_request_method(case["password"])
            
            with pytest.raises(ValueError) as excinfo:
                self._registration_method(service, request)
            
            error = str(excinfo.value).lower()
            assert "password" in error
            assert case["expected"].lower() in error