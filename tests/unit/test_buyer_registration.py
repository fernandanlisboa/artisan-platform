from unittest.mock import Mock
import uuid
from app.application.services.user_registration_service import UserRegistrationService
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.repositories.buyer_repository_interface import IBuyerRepository
from app.domain.repositories.address_repository_interface import IAddressRepository
from tests.unit.mock_data import MockFactory

from app.presentation.dtos.user_dtos import RegisterBuyerRequest, RegisterAddressRequest



class TestBuyerRegistration:
    
    def test_register_buyer_successfully(self):
        # Create mock repositories
        mock_user_repository = Mock(spec=IUserRepository)
        mock_buyer_repository = Mock(spec=IBuyerRepository)
        mock_address_repository = Mock(spec=IAddressRepository)
        
        # Create the service with mock repositories
        service = UserRegistrationService(
            user_repository=mock_user_repository,
            artisan_repository=Mock(),  # Not used in this test
            address_repository=mock_address_repository,
            buyer_repository=mock_buyer_repository
        )
        
        # Gere IDs específicos que você precisará usar em múltiplos lugares
        user_id = str(uuid.uuid4())
        address_id = str(uuid.uuid4())
        print(address_id)
        # Configure os retornos dos mocks usando a factory
        mock_address_repository.save.return_value = MockFactory().create_address({'address_id': address_id})
        mock_user_repository.save.return_value = MockFactory().create_user({
            'user_id': user_id, 
            'address_id': address_id,
            'email': 'buyer@example.com'  # Adicione esta linha para garantir o mesmo email
        })
        mock_buyer_repository.save.return_value = MockFactory().create_buyer({
            'buyer_id': user_id,
            'full_name': 'John Doe',  # Garanta que o nome também corresponda
            'phone': '9876543210'
        })
        
        # Dados de entrada também podem ser gerados pela factory
        # (ou usar um objeto fixo como você tinha antes, se preferir)
        buyer_data = {
            'email': 'buyer@example.com',
            'password': 'SecurePassword123',
            'full_name': 'John Doe',
            'phone': '9876543210',
            'address': {
                'street': 'Main Street',
                'number': '123',
                'complement': 'Apt 4B',
                'neighborhood': 'Downtown', 
                'city': 'Test City',
                'state': 'TS',
                'zip_code': '12345-678',
                'country': 'Test Country'
            }
        }
        
        # Call the service method with the dictionary
        buyer_request = RegisterBuyerRequest(**buyer_data)
        response = service.register_buyer(buyer_request)
        
        # Assertions
        assert response.user_id == user_id
        assert response.email == mock_user_repository.save.return_value.email
        assert response.full_name == mock_buyer_repository.save.return_value.full_name
        
        # Verify the repositories were called
        mock_address_repository.save.assert_called_once()
        mock_user_repository.save.assert_called_once()
        mock_buyer_repository.save.assert_called_once()
        
    #TODO registro com email ja existente
    #TODO registro com senha fraca
    #TODO registro com dados inválidos (name, phone)