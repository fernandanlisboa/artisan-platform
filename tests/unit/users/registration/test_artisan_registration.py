import pytest
from tests.unit.users.registration.base_registration_test import BaseRegistrationTest
from app.presentation.dtos.user_dtos import RegisterArtisanRequest

class TestArtisanRegistration(BaseRegistrationTest):
    """Testes para o registro de artesãos."""
    
    def _registration_method(self, service, request):
        """Define o método de registro específico para artesãos."""
        return service.register_artisan(request)
    
    @pytest.fixture
    def valid_artisan_request(self):
        """Cria uma requisição válida de artesão."""
        from tests.unit.users.registration.base_registration_test import mock_factory
        valid_artisan_request = mock_factory.artisan.create()
        
        return {
            'store_name': valid_artisan_request.store_name,
            'phone': valid_artisan_request.phone,
            'bio': valid_artisan_request.bio            
        }
    
    def test_register_user_successfully(self, service, mock_repositories, 
                                     valid_artisan_request, valid_user_request, valid_address_request, mock_entities, test_ids):
        """Testa o registro bem-sucedido de um artesão."""
        request = RegisterArtisanRequest(**valid_artisan_request, **valid_user_request, **valid_address_request)
        
        # Arrange
        self._setup_successful_registration(mock_repositories, mock_entities, 'artisan', request)
        
        # Act
        result = self._registration_method(service, request)
        
        # Assert
        self._assert_successful_registration(result, request, mock_repositories, test_ids, 'artisan')
