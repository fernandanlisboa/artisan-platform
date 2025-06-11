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

from app.presentation.dtos.user_dtos import RegisterBuyerRequest, RegisterAddressRequest
from tests.unit.base_user_registration_test import BaseUserRegistrationTest


class TestBuyerRegistration(BaseUserRegistrationTest):
    
    def _registration_method(self, service, request):
        """Define o método de registro específico para compradores."""
        return service.register_buyer(request)
    
    @pytest.fixture
    def valid_buyer_request(self, valid_address_request):
        """Cria um objeto de requisição de comprador válido com senha forte."""
        return RegisterBuyerRequest(
            email=fake.email(),
            password=f"Valid{fake.random_int(10, 99)}Password!{fake.random_letter().upper()}",
            full_name=fake.name(),
            phone=self._generate_valid_phone(),
            address=valid_address_request
        )
    
    @pytest.fixture
    def mock_entities(self, test_ids, valid_buyer_request):
        """Configura entidades mock específicas para compradores."""
        return {
            'address': MockFactory().create_address({
                'address_id': test_ids['address_id'],
                'street': valid_buyer_request.address.street,
                'number': valid_buyer_request.address.number,
                'complement': valid_buyer_request.address.complement,
                'neighborhood': valid_buyer_request.address.neighborhood,
                'city': valid_buyer_request.address.city,
                'state': valid_buyer_request.address.state,
                'zip_code': valid_buyer_request.address.zip_code,
                'country': valid_buyer_request.address.country
            }),
            'user': MockFactory().create_user({
                'user_id': test_ids['user_id'],
                'email': valid_buyer_request.email,
                'address_id': test_ids['address_id']
            }),
            'buyer': MockFactory().create_buyer({
                'buyer_id': test_ids['user_id'],
                'full_name': valid_buyer_request.full_name,
                'phone': valid_buyer_request.phone
            })
        }
    
    def test_register_buyer_successfully(self, mock_repositories, service, valid_buyer_request, 
                                        mock_entities, test_ids):
        """Testa o fluxo de sucesso do registro de comprador."""
        # Arrange
        self._setup_basic_mocks(mock_repositories, mock_entities)
        mock_repositories['buyer_repo'].save.return_value = mock_entities['buyer']
        
        # Act
        response = service.register_buyer(valid_buyer_request)
        
        # Assert
        assert response.user_id == test_ids['user_id']
        assert response.email == valid_buyer_request.email
        assert response.full_name == valid_buyer_request.full_name
        
        # Verifica chamadas aos repositórios
        mock_repositories['user_repo'].get_by_email.assert_called_once()
        mock_repositories['address_repo'].get_by_attributes.assert_called_once()
        mock_repositories['user_repo'].save.assert_called_once()
        mock_repositories['buyer_repo'].save.assert_called_once()
    
    def test_register_buyer_with_existing_address(self, mock_repositories, service, 
                                                valid_buyer_request, mock_entities, test_ids):
        """Testa registro com um endereço já existente."""
        # Arrange
        self._setup_basic_mocks(mock_repositories, mock_entities, address_exists=True)
        mock_repositories['buyer_repo'].save.return_value = mock_entities['buyer']
        
        # Act
        response = service.register_buyer(valid_buyer_request)
        
        # Assert
        mock_repositories['address_repo'].save.assert_not_called()
        user_arg = mock_repositories['user_repo'].save.call_args[0][0]
        assert user_arg.address_id == test_ids['address_id']
    
    def test_register_buyer_with_existing_email(self, mock_repositories, service, 
                                              valid_buyer_request, mock_entities):
        """Testa validação de email duplicado."""
        self._setup_basic_mocks(mock_repositories, mock_entities, email_exists=True)
        self._assert_common_validations(
            service, valid_buyer_request, mock_repositories, "Email already registered")
    
    @pytest.mark.parametrize("invalid_email", [
        "plainaddress",       # Sem @ e domínio
        "@missinglocal.org",  # Sem parte local
        "user@.com",          # Domínio inválido
        "user@domain",        # Sem TLD
    ])
    def test_register_buyer_with_invalid_email(self, mock_repositories, service, invalid_email):
        """Testa validação de email inválido."""
        request = RegisterBuyerRequest(
            email=invalid_email,
            password=f"Valid{fake.random_int(10, 99)}Password!{fake.random_letter().upper()}",
            full_name=fake.name(),
            phone=self._generate_valid_phone(),
            address=MockFactory().create_address()
        )
        self._assert_common_validations(
            service, request, mock_repositories, "Invalid email format")
    
    def test_register_buyer_with_invalid_password(self, mock_repositories, service):
        """Testa diferentes formatos de senha inválida usando o método da classe base."""
        def create_request(password):
            request = Mock()
            request.email = fake.email()
            request.password = password
            request.full_name = fake.name()
            return request
            
        self._test_password_validations(service, mock_repositories, create_request)