from unittest.mock import Mock
import uuid
from app.application.services.user_registration_service import UserRegistrationService
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app.domain.repositories.address_repository_interface import IAddressRepository
from tests.unit.mock_data import MockFactory
from app.presentation.dtos.user_dtos import RegisterArtisanRequest, RegisterAddressRequest
from app.domain.models.user import UserEntity 
from app.domain.models.artisan import ArtisanEntity

class TestArtisanRegistration:
  
    def test_register_artisan_successfully(self):
        # Create mock repositories
        mock_user_repository = Mock(spec=IUserRepository)
        mock_artisan_repository = Mock(spec=IArtisanRepository)
        mock_address_repository = Mock(spec=IAddressRepository)
        
        # Create the service with mock repositories
        service = UserRegistrationService(
            user_repository=mock_user_repository,
            artisan_repository=mock_artisan_repository,
            address_repository=mock_address_repository,
            buyer_repository=Mock()  # Not used in this test
        )
        
        # Gere IDs específicos que você precisará usar em múltiplos lugares
        user_id = str(uuid.uuid4())
        address_id = str(uuid.uuid4())
        
        # Configure os retornos dos mocks usando a factory
        mock_user_repository.save.return_value = MockFactory().create_user({
            'user_id': user_id,
            'email': 'test@artisan.com',
            'status': 'active',
            'address_id': address_id
        })
        
        mock_artisan_repository.save.return_value = MockFactory().create_artisan({
            'artisan_id': user_id,
            'store_name': 'My Test Shop',
            'phone': '1234567890',
            'bio': 'Handmade goods',
            'status': 'active'
        })
        
        # Optional: Add address repository mock if needed
        mock_address_repository.save.return_value = MockFactory().create_address({'address_id': address_id})
        
        # Create input data - use DTO pattern like in buyer test
        artisan_data = {
            'email': 'test@artisan.com',
            'password': 'SecurePassword123',
            'store_name': 'My Test Shop',
            'phone': '1234567890',
            'bio': 'Handmade goods',
            'address': {
                'street': 'Artisan Street',
                'number': '456',
                'complement': 'Studio 7',
                'neighborhood': 'Craft District',
                'city': 'Artville',
                'state': 'AR',
                'zip_code': '54321-876',
                'country': 'Artland'
            }
        }
        
        # Convert to DTO object
        artisan_request = RegisterArtisanRequest(**artisan_data)
        
        # Call the service method
        response = service.register_artisan(artisan_request)
        
        # Assertions
        assert response.user_id == user_id
        assert response.email == mock_user_repository.save.return_value.email
        assert response.store_name == mock_artisan_repository.save.return_value.store_name
        
        # Verify repository calls
        mock_user_repository.save.assert_called_once()
        mock_artisan_repository.save.assert_called_once()
        mock_address_repository.save.assert_called_once()
        
        # Optional: More detailed assertions on the arguments passed to repositories
        saved_user_arg = mock_user_repository.save.call_args[0][0]
        assert isinstance(saved_user_arg, UserEntity)
        assert saved_user_arg.email == 'test@artisan.com'
        
        saved_artisan_arg = mock_artisan_repository.save.call_args[0][0]
        assert isinstance(saved_artisan_arg, ArtisanEntity)
        assert saved_artisan_arg.store_name == 'My Test Shop'
        assert saved_artisan_arg.phone == '1234567890'
        
    #TODO registro com email ja existente
    #TODO registro com senha fraca
    #TODO registro com dados inválidos (store_name, phone, bio)