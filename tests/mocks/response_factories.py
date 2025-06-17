
from app.presentation.dtos.product_dtos import CategoryDTO, ResponseRegisterProduct
from app.presentation.dtos.user_dtos import ArtisanRegistrationResponse, BuyerRegistrationResponse, AddressResponse
from datetime import datetime, timezone
import uuid

class ResponseFactory:
    """Factory para criar DTOs de resposta usando os DTOs reais da aplicação."""
    
    @staticmethod
    def create_product_response(**kwargs):
        """Cria um ResponseRegisterProduct pré-preenchido."""
        from tests.mocks.factories import MockFactory
        
        product = MockFactory().product.create()
        category = MockFactory().category.create()
        
        # Substituir valores padrões com os fornecidos em kwargs
        product_id = kwargs.get('product_id', product.product_id)
        name = kwargs.get('name', product.name)
        
        # Criar o DTO de resposta real
        return ResponseRegisterProduct(
            product_id=product_id,
            name=name,
            description=kwargs.get('description', product.description),
            price=kwargs.get('price', product.price),
            stock=kwargs.get('stock', product.stock),
            artisan_id=kwargs.get('artisan_id', str(uuid.uuid4())),
            image_url=kwargs.get('image_url', None),
            registration_date=kwargs.get('registration_date', datetime.now(timezone.utc)),
            status=kwargs.get('status', 'active'),
            category=CategoryDTO(
                category_id=kwargs.get('category_id', category.category_id),
                name=kwargs.get('category_name', category.name),
                description=kwargs.get('category_description', category.description)
            )
        )
    
    @staticmethod
    def create_artisan_response(**kwargs):
        """Cria um ArtisanRegistrationResponse pré-preenchido."""
        from tests.mocks.factories import MockFactory
        
        artisan = MockFactory().artisan.create()
        user = MockFactory().user.create()
        
        # Criar endereço opcional
        address_data = None
        if kwargs.get('with_address', True):
            address = MockFactory().address.create()
            address_data = AddressResponse(
                address_id=address.address_id,
                street=address.street,
                number=address.number,
                complement=address.complement,
                neighborhood=address.neighborhood,
                city=address.city,
                state=address.state,
                zip_code=address.zip_code,
                country=address.country
            )
        
        return ArtisanRegistrationResponse(
            user_id=kwargs.get('user_id', user.user_id),
            email=kwargs.get('email', user.email),
            store_name=kwargs.get('store_name', artisan.store_name),
            phone=kwargs.get('phone', artisan.phone),
            bio=kwargs.get('bio', artisan.bio),
            status=kwargs.get('status', 'active'),
            address=address_data,
            registration_date=kwargs.get('registration_date', datetime.now(timezone.utc))
        )