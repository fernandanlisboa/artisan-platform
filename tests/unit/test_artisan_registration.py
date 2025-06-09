from unittest.mock import Mock, patch
import uuid
from app.application.services.user_registration_service import UserRegistrationService
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app.domain.repositories.address_repository_interface import IAddressRepository
from tests.unit.mock_data import MockFactory, MockAddressEntity, MockUserEntity, MockArtisanEntity
from app.presentation.dtos.user_dtos import RegisterArtisanRequest, RegisterAddressRequest
from app.domain.models.user import UserEntity 
from app.domain.models.artisan import ArtisanEntity

class TestArtisanRegistration:
  
    def test_register_artisan_successfully(self):
        # Create mock repositories
        mock_user_repository = Mock(spec=IUserRepository)
        mock_artisan_repository = Mock(spec=IArtisanRepository)
        mock_address_repository = Mock(spec=IAddressRepository)
        # Adicionado mock de buyer repository
        
        # Create the service with mock repositories
        service = UserRegistrationService(
            user_repository=mock_user_repository,
            artisan_repository=mock_artisan_repository,
            address_repository=mock_address_repository,
       )
        
        # Gere IDs específicos que você precisará usar em múltiplos lugares
        user_id = str(uuid.uuid4())
        address_id = str(uuid.uuid4())
        
        # Create complete mock objects with proper properties
        mock_address = MockAddressEntity(
            address_id=address_id,
            street="Artisan Street",
            number="456",
            complement="Studio 7",
            neighborhood="Craft District",
            city="Artville",
            state="AR",
            zip_code="54321-876",
            country="Artland"
        )
        
        mock_user = MockUserEntity(
            user_id=user_id,
            email='test@artisan.com',
            password='SecurePassword123',
            status='active',
            address_id=address_id
        )
        
        mock_artisan = MockArtisanEntity(
            artisan_id=user_id,
            store_name='My Test Shop',
            phone='1234567890',
            bio='Handmade goods',
            status='active'
        )
        
        # Configure mock returns
        # Para o address: primeiro get_by_attributes retorna None (não encontrado)
        # depois save cria o novo endereço
        mock_address_repository.get_by_attributes.return_value = None
        mock_address_repository.save.return_value = mock_address
        
        # User e Artisan salvos
        mock_user_repository.save.return_value = mock_user
        mock_artisan_repository.save.return_value = mock_artisan
        
        # Create address request
        address_request = RegisterAddressRequest(
            street="Artisan Street",
            number="456",
            complement="Studio 7",
            neighborhood="Craft District",
            city="Artville",
            state="AR",
            zip_code="54321-876",
            country="Artland"
        )
        
        # Create artisan request with nested address
        artisan_data = {
            'email': 'test@artisan.com',
            'password': 'SecurePassword123',
            'store_name': 'My Test Shop',
            'phone': '1234567890',
            'bio': 'Handmade goods',
            'address': address_request  # Objeto Pydantic real, não um dicionário
        }
        
        # Convert to DTO object
        artisan_request = RegisterArtisanRequest(**artisan_data)
        
        # Call the service method
        response = service.register_artisan(artisan_request)
        
        # Assertions
        assert response.user_id == user_id
        assert response.email == 'test@artisan.com'
        assert response.store_name == 'My Test Shop'
        
        # Verify repository calls
        mock_address_repository.get_by_attributes.assert_called_once()
        mock_address_repository.save.assert_called_once()
        mock_user_repository.save.assert_called_once()
        mock_artisan_repository.save.assert_called_once()
        
        # Optional: More detailed assertions on the arguments passed to repositories
        saved_user_arg = mock_user_repository.save.call_args[0][0]
        assert isinstance(saved_user_arg, UserEntity)
        assert saved_user_arg.email == 'test@artisan.com'
        
        saved_artisan_arg = mock_artisan_repository.save.call_args[0][0]
        assert isinstance(saved_artisan_arg, ArtisanEntity)
        assert saved_artisan_arg.store_name == 'My Test Shop'
        assert saved_artisan_arg.phone == '1234567890'
    
    def test_register_artisan_with_existing_address(self):
        # Create mock repositories
        mock_user_repository = Mock(spec=IUserRepository)
        mock_artisan_repository = Mock(spec=IArtisanRepository)
        mock_address_repository = Mock(spec=IAddressRepository)
        
        # Create the service with mock repositories
        service = UserRegistrationService(
            user_repository=mock_user_repository,
            artisan_repository=mock_artisan_repository,
            address_repository=mock_address_repository,
        )
        
        # Gere IDs específicos que você precisará usar em múltiplos lugares
        user_id = str(uuid.uuid4())
        address_id = str(uuid.uuid4())
        
        # Create complete mock objects with proper properties
        mock_existing_address = MockAddressEntity(
            address_id=address_id,
            street="Artisan Street",
            number="456",
            complement="Studio 7",
            neighborhood="Craft District",
            city="Artville",
            state="AR",
            zip_code="54321-876",
            country="Artland"
        )
        
        mock_user = MockUserEntity(
            user_id=user_id,
            email='test@artisan.com',
            password='SecurePassword123',
            status='active',
            address_id=address_id
        )
        
        mock_artisan = MockArtisanEntity(
            artisan_id=user_id,
            store_name='My Test Shop',
            phone='1234567890',
            bio='Handmade goods',
            status='active'
        )
        
        # Configure mock returns
        # A diferença principal: get_by_attributes RETORNA um endereço existente
        mock_address_repository.get_by_attributes.return_value = mock_existing_address
        
        # User e Artisan salvos
        mock_user_repository.save.return_value = mock_user
        mock_artisan_repository.save.return_value = mock_artisan
        
        # Create address request (mesmos dados do endereço existente)
        address_request = RegisterAddressRequest(
            street="Artisan Street",
            number="456",
            complement="Studio 7",
            neighborhood="Craft District",
            city="Artville",
            state="AR",
            zip_code="54321-876",
            country="Artland"
        )
        
        # Create artisan request with nested address
        artisan_data = {
            'email': 'test@artisan.com',
            'password': 'SecurePassword123',
            'store_name': 'My Test Shop',
            'phone': '1234567890',
            'bio': 'Handmade goods',
            'address': address_request
        }
        
        # Convert to DTO object
        artisan_request = RegisterArtisanRequest(**artisan_data)
        
        # Call the service method
        response = service.register_artisan(artisan_request)
        
        # Assertions
        assert response.user_id == user_id
        assert response.email == 'test@artisan.com'
        assert response.store_name == 'My Test Shop'
        
        # Verify repository calls
        mock_address_repository.get_by_attributes.assert_called_once()
        # Não deve salvar um novo endereço, pois um já foi encontrado
        mock_address_repository.save.assert_not_called()
        mock_user_repository.save.assert_called_once()
        mock_artisan_repository.save.assert_called_once()
        
        # Verificar se o user foi criado com o address_id do endereço existente
        saved_user_arg = mock_user_repository.save.call_args[0][0]
        assert saved_user_arg.address_id == address_id

    #TODO registro com email ja existente
    #TODO registro com senha fraca
    #TODO registro com dados inválidos (store_name, phone, bio)