import pytest
from unittest.mock import Mock
import uuid
import random
from app.application.services.user_registration_service import UserRegistrationService
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app.domain.repositories.address_repository_interface import IAddressRepository
from app.domain.repositories.buyer_repository_interface import IBuyerRepository

from tests.unit.mock_data import MockFactory, fake
from tests.unit.base_user_registration_test import BaseUserRegistrationTest
from app.presentation.dtos.user_dtos import RegisterArtisanRequest

class TestArtisanRegistration(BaseUserRegistrationTest):
    
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

    def __generate_valid_phone(self, max_length=20):
        """Gera um número de telefone válido com comprimento máximo especificado."""
        # Formatos simples que cabem em 20 caracteres
        formats = [
            '+## (##) ####-####',
            '(##) ####-####',
            '##-####-####',
            '+##########'
        ]
        
        # Escolhe um formato aleatório
        format_template = random.choice(formats)
        
        # Substitui # por dígitos aleatórios - CORRIGIDO: converte o dígito para string
        phone = ''.join([str(fake.random_digit()) if c == '#' else c for c in format_template])
        
        return phone

    def _registration_method(self, service, request):
        """Define o método de registro específico para artesãos."""
        return service.register_artisan(request)
    
    @pytest.fixture
    def valid_artisan_request(self, valid_address_request):
        """Cria um objeto de requisição de artesão válido."""
        return RegisterArtisanRequest(
            email=fake.email(),
            password=f"Valid{fake.random_int(10, 99)}Password!{fake.random_letter().upper()}",
            store_name=f"Ateliê {fake.company()}",
            phone=self._generate_valid_phone(),
            bio=fake.paragraph(),
            address=valid_address_request
        )
    
    @pytest.fixture
    def mock_entities(self, test_ids, valid_artisan_request):
        """Configura entidades mock consistentes para os testes."""
        return {
            'address': MockFactory().create_address({
                'address_id': test_ids['address_id'],
                'street': valid_artisan_request.address.street,
                'number': valid_artisan_request.address.number,
                'complement': valid_artisan_request.address.complement,
                'neighborhood': valid_artisan_request.address.neighborhood,
                'city': valid_artisan_request.address.city,
                'state': valid_artisan_request.address.state,
                'zip_code': valid_artisan_request.address.zip_code,
                'country': valid_artisan_request.address.country
            }),
            'user': MockFactory().create_user({
                'user_id': test_ids['user_id'],
                'email': valid_artisan_request.email,
                'address_id': test_ids['address_id']
            }),
            'artisan': MockFactory().create_artisan({
                'artisan_id': test_ids['user_id'],
                'store_name': valid_artisan_request.store_name,
                'phone': valid_artisan_request.phone,
                'bio': valid_artisan_request.bio
            })
        }
    
    def setup_successful_registration(self, mock_repositories, mock_entities):
        """Configura mocks para um registro bem-sucedido."""
        mock_repositories['user_repo'].get_by_email.return_value = None
        mock_repositories['address_repo'].get_by_attributes.return_value = None
        mock_repositories['address_repo'].save.return_value = mock_entities['address']
        mock_repositories['user_repo'].save.return_value = mock_entities['user']
        mock_repositories['artisan_repo'].save.return_value = mock_entities['artisan']
    
    def setup_existing_email(self, mock_repositories, mock_entities):
        """Configura mocks para o cenário de e-mail já existente."""
        mock_repositories['user_repo'].get_by_email.return_value = mock_entities['user']
    
    def setup_existing_address(self, mock_repositories, mock_entities):
        """Configura mocks para o cenário de endereço já existente."""
        mock_repositories['user_repo'].get_by_email.return_value = None
        mock_repositories['address_repo'].get_by_attributes.return_value = mock_entities['address']
        mock_repositories['user_repo'].save.return_value = mock_entities['user']
        mock_repositories['artisan_repo'].save.return_value = mock_entities['artisan']
    
    def test_register_artisan_successfully(self, mock_repositories, service, valid_artisan_request, 
                                          mock_entities, test_ids):
        """Testa o fluxo de sucesso do registro de artesão."""
        # Arrange
        self.setup_successful_registration(mock_repositories, mock_entities)
        
        # Act
        response = service.register_artisan(valid_artisan_request)
        
        # Assert
        assert response.user_id == test_ids['user_id']
        assert response.email == valid_artisan_request.email
        assert response.store_name == valid_artisan_request.store_name
        
        # Verifica chamadas aos repositórios
        mock_repositories['user_repo'].get_by_email.assert_called_once()
        mock_repositories['address_repo'].get_by_attributes.assert_called_once()
        mock_repositories['user_repo'].save.assert_called_once()
        mock_repositories['artisan_repo'].save.assert_called_once()
    
    def test_register_artisan_with_existing_address(self, mock_repositories, service, 
                                                  valid_artisan_request, mock_entities, test_ids):
        """Testa registro com um endereço já existente."""
        # Arrange
        self.setup_existing_address(mock_repositories, mock_entities)
        
        # Act
        response = service.register_artisan(valid_artisan_request)
        
        # Assert - foco apenas no comportamento de endereço
        mock_repositories['address_repo'].get_by_attributes.assert_called_once()
        mock_repositories['address_repo'].save.assert_not_called()
        
        # Verifica que o usuário foi associado ao endereço existente
        user_arg = mock_repositories['user_repo'].save.call_args[0][0]
        assert user_arg.address_id == test_ids['address_id']
    
    def test_register_artisan_with_existing_email(self, mock_repositories, service, 
                                                valid_artisan_request, mock_entities):
        """Testa validação de email duplicado."""
        # Arrange
        self.setup_existing_email(mock_repositories, mock_entities)
        
        # Act & Assert
        with pytest.raises(ValueError) as excinfo:
            service.register_artisan(valid_artisan_request)
        
        assert "Email already registered" in str(excinfo.value)
        
        # Verifica que nada foi salvo
        mock_repositories['user_repo'].save.assert_not_called()
        mock_repositories['address_repo'].save.assert_not_called()
        mock_repositories['artisan_repo'].save.assert_not_called()
    
    def test_register_artisan_with_invalid_password(self, mock_repositories, service):
        """Testa diferentes formatos de senha inválida."""
        # Configurar mock para email não existente
        mock_repositories['user_repo'].get_by_email.return_value = None
        
        # Casos de teste com senha inválida e mensagens específicas esperadas
        test_cases = [
            {"password": "short", "expected": "8 characters"},  # Verificar limite mínimo
            {"password": "nouppercase123$", "expected": "uppercase"},
            {"password": "NOLOWERCASE123$", "expected": "lowercase"},
            {"password": "NoNumbers$", "expected": "number"},
            {"password": "NoSpecialChars123", "expected": "special character"}
        ]
        
        for case in test_cases:
            # Cria mock request com a senha do caso de teste
            mock_request = Mock()
            mock_request.email = fake.email()
            mock_request.password = case["password"]
            mock_request.store_name = fake.company()
            
            # Act & Assert
            with pytest.raises(ValueError) as excinfo:
                service.register_artisan(mock_request)
            
            # Valida a mensagem específica para cada tipo de senha inválida
            error = str(excinfo.value).lower()
            assert "password" in error, f"Erro para '{case['password']}' não menciona 'password'"
            assert case["expected"].lower() in error, f"Erro para '{case['password']}' não contém '{case['expected']}'"
