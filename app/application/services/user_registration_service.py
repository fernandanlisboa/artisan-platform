# app/application/services/user_registration_service.py
# ...
from app.domain.repositories.address_repository_interface import IAddressRepository # Importe a interface
from app.domain.models.address import AddressEntity as Address # Importe a entidade pura Address
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app.presentation.dtos.user_dtos import RegisterArtisanRequest, ArtisanRegistrationResponse
from app.domain.models.user import UserEntity as User # Importe a entidade pura User
from app.domain.models.artisan import ArtisanEntity # Importe a entidade pura Artisan
class UserRegistrationService:
    """
    Service responsible for user registration in the platform.
    
    This service manages the registration flow for artisans and buyers,
    performing data validation, creating entities, and persisting them
    through appropriate repositories.
    """
    
    def __init__(self, user_repository: IUserRepository, artisan_repository: IArtisanRepository, address_repository: IAddressRepository, buyer_repository=None):
        """
        Initialize the registration service with required repositories.
        
        Args:
            user_repository: Repository for user operations
            artisan_repository: Repository for artisan operations
            address_repository: Repository for address operations
            buyer_repository: Repository for buyer operations (optional)
        """
        self.user_repository = user_repository
        self.artisan_repository = artisan_repository
        self.address_repository = address_repository
        self.buyer_repository = buyer_repository
    
    def __check_password_validity(self, password: str) -> tuple[bool, str]:
        #TODO: add error classes for better error handling
        """
        Check if the password meets the required criteria.
        Returns (is_valid, error_message).
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one number"
        
        if not any(char.islower() for char in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(not char.isalnum() for char in password):
            return False, "Password must contain at least one special character"
        
        return True, ""
    
    def register_artisan(self, request_data: RegisterArtisanRequest) -> ArtisanRegistrationResponse:
        """
        Register a new artisan in the platform.
        
        Implements the complete artisan registration flow:
        1. Checks if the address already exists or creates a new one
        2. Validates if the email is already registered
        3. Verifies password strength
        4. Creates and persists user and artisan entities
        
        Args:
            request_data: DTO containing the artisan registration data
            
        Returns:
            ArtisanRegistrationResponse: DTO with the registered artisan data
            
        Raises:
            ValueError: If the email is already registered or the password is invalid
        """
        #TODO: add error classes for better error handling
        address_entity = Address(
            address_id=None,  # ID será gerado
            street=request_data.address.street,
            number=request_data.address.number,
            state=request_data.address.state,
            city=request_data.address.city,
            neighborhood=request_data.address.neighborhood,
            complement=request_data.address.complement,
            country=request_data.address.country,
            zip_code=request_data.address.zip_code
        )
        print("Address Entity: ", address_entity)
        #check if the address already exists
        saved_address = self.address_repository.get_by_attributes(address_entity)
        if saved_address:
            print("Address already exists, using existing address.")
        else:
            saved_address = self.address_repository.save(address_entity)
            print("New address saved: ", saved_address)
        
        #check email already exists
        if self.user_repository.get_by_email(request_data.email) is not None:
            raise ValueError("Email already registered.")
        
        user_entity = User(
            user_id=None,  # ID será gerado
            email=request_data.email,
            password=request_data.password,  # Aqui você deve aplicar a lógica de hash da senha
            status='active',  # Status do usuário, pode ser 'active', 'inactive', etc.
            address_id=saved_address.address_id,  # Inicialmente None, será atualizado após salvar o endereço
        )
        print("User Entity: ", user_entity)
        
        
        #check if the password is valid
        is_valid, error_message = self.__check_password_validity(request_data.password)
        if not is_valid:
            raise ValueError(error_message)
        
        saved_user_entity = self.user_repository.save(user_entity)
        
        #check phone
        artisan_entity = ArtisanEntity(
            artisan_id=saved_user_entity.user_id,
            bio=request_data.bio,
            store_name=request_data.store_name,
            phone=request_data.phone
        )
        
        print("Artisan Entity: ", artisan_entity)
        saved_artisan_entity = self.artisan_repository.save(artisan_entity)
        
        return ArtisanRegistrationResponse.from_domain_entities(saved_artisan_entity, saved_user_entity, saved_address)