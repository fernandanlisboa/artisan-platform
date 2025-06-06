# ...
from app.domain.repositories.address_repository_interface import IAddressRepository
from app.domain.models.address import AddressEntity as Address
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app.domain.repositories.buyer_repository_interface import IBuyerRepository # NOVO: Importe a interface do repositório de comprador
from app.presentation.dtos.user_dtos import RegisterArtisanRequest, ArtisanRegistrationResponse
from app.presentation.dtos.user_dtos import RegisterBuyerRequest, BuyerRegistrationResponse # NOVO: DTOs para o comprador
from app.domain.models.user import UserEntity as User
from app.domain.models.artisan import ArtisanEntity
from app.domain.models.buyer import BuyerEntity # NOVO: Importe a entidade pura Buyer


class UserRegistrationService:
    def __init__(self, user_repository: IUserRepository, artisan_repository: IArtisanRepository, address_repository: IAddressRepository, buyer_repository: IBuyerRepository): # NOVO: buyer_repository
        self.user_repository = user_repository
        self.artisan_repository = artisan_repository
        self.address_repository = address_repository
        self.buyer_repository = buyer_repository # NOVO: atributo
        # ...

    def register_artisan(self, request_data: RegisterArtisanRequest) -> ArtisanRegistrationResponse:
        # Se dados de endereço forem fornecidos, crie e salve o endereço
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

        saved_address = self.address_repository.save(address_entity)
        user_entity = User(
            user_id=None,  # ID será gerado
            email=request_data.email,
            password=request_data.password,  # Aqui você deve aplicar a lógica de hash da senha
            status='active',  # Status do usuário, pode ser 'active', 'inactive', etc.
            address_id=saved_address.address_id,  # Inicialmente None, será atualizado após salvar o endereço
        )
        print("User Entity: ", user_entity)
        saved_user_entity = self.user_repository.save(user_entity) # Salva o usuário (agora com address_id)

        artisan_entity = ArtisanEntity(
            artisan_id=saved_user_entity.user_id,
            bio=request_data.bio,
            store_name=request_data.store_name,
            phone=request_data.phone
        )

        print("Artisan Entity: ", artisan_entity)
        saved_artisan_entity = self.artisan_repository.save(artisan_entity)

        return ArtisanRegistrationResponse.from_domain_entities(saved_artisan_entity, saved_user_entity, saved_address)

    def register_buyer(self, request_data: RegisterBuyerRequest) -> BuyerRegistrationResponse:
        """
        Registra um novo comprador no sistema.
        Cria e salva o endereço, o usuário e a entidade do comprador.
        """
        # Se dados de endereço forem fornecidos, crie e salve o endereço
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
        print("Address Entity (Buyer): ", address_entity)

        saved_address = self.address_repository.save(address_entity)
        user_entity = User(
            user_id=None,  # ID será gerado
            email=request_data.email,
            password=request_data.password,  # Aqui você deve aplicar a lógica de hash da senha
            status='active',  # Status do usuário, pode ser 'active', 'inactive', etc.
            address_id=saved_address.address_id,  # Vincula o endereço salvo ao usuário
        )
        print("User Entity (Buyer): ", user_entity)
        saved_user_entity = self.user_repository.save(user_entity) # Salva o usuário (agora com address_id)

        buyer_entity = BuyerEntity(
            buyer_id=saved_user_entity.user_id, # O ID do comprador é o mesmo ID do usuário
            full_name=request_data.full_name,
            phone=request_data.phone,
            address=request_data.address
        )

        print("Buyer Entity: ", buyer_entity)
        saved_buyer_entity = self.buyer_repository.save(buyer_entity)

        return BuyerRegistrationResponse.from_domain_entities(saved_buyer_entity, saved_user_entity, saved_address)