import pytest
from tests.unit.users.registration.base_registration_test import BaseRegistrationTest
from app.presentation.dtos.user_dtos import RegisterBuyerRequest

class TestBuyerRegistration(BaseRegistrationTest):
    """Testes para o registro de compradores."""
    
    def _registration_method(self, service, request):
        """Define o método de registro específico para compradores."""
        return service.register_buyer(request)
    
    @pytest.fixture
    def valid_buyer_request(self):
        """Cria uma requisição válida de comprador."""
        from tests.unit.users.registration.base_registration_test import mock_factory
        valid_buyer_request = mock_factory.buyer.create()
        
        return {
            'full_name': valid_buyer_request.full_name,
            'phone': valid_buyer_request.phone
        }
    
    def test_register_user_successfully(self, service, mock_repositories, 
                                     valid_user_request, valid_buyer_request, valid_address_request, mock_entities, test_ids):
        """Testa o registro bem-sucedido de um comprador."""
        request = RegisterBuyerRequest(**valid_user_request, **valid_buyer_request, **valid_address_request)
        
        # Arrange
        # Passe o objeto request como quarto parâmetro
        self._setup_successful_registration(mock_repositories, mock_entities, 'buyer', request)
        
        # Act
        result = self._registration_method(service, request)
        
        # Assert
        self._assert_successful_registration(result, request, mock_repositories, test_ids, 'buyer')


    def test_register_user_duplicate_email(self, service, mock_repositories, 
                                       valid_user_request, valid_buyer_request, valid_address_request, mock_entities):
        """Testa a tentativa de registrar um comprador com email já existente."""
        request = RegisterBuyerRequest(**valid_user_request, **valid_buyer_request, **valid_address_request)
        
        self._test_duplicate_email(service, mock_repositories, request, mock_entities)