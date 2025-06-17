from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from app.domain.repositories.product_repository_interface import IProductRepository
from app.domain.repositories.category_repository_interface import ICategoryRepository
from app.domain.models.product import ProductEntity
from app.presentation.dtos.product_dtos import RegisterProductRequest, ResponseRegisterProduct
class ArtisanProductService:
    def __init__(self, product_repository: IProductRepository, category_repository: ICategoryRepository, artisan_repository: IArtisanRepository):
        self._artisan_repository = artisan_repository
        self.product_repository = product_repository
        self.category_repository = category_repository      

    def create_artisan_product(self, artisan_id: str, product_data: RegisterProductRequest) -> ResponseRegisterProduct:
        artisan = self._artisan_repository.get_artisan_by_id(artisan_id)
        #TODO: exceptionError
        if not artisan:
            raise ValueError("Artisan not found")

        new_product = ProductEntity(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock if product_data.stock is not None else 0,
            artisan_id=artisan_id,
            image_url=product_data.image_url if product_data.image_url else None,
            category_id=product_data.category_id,
        )
        
        #check category_id 
        category = self.category_repository.get_by_id(new_product.category_id)
        if not category:
            raise ValueError("Category does not exist")
        print(f"category found: {category}")
        # Validate price and name
        if not product_data.name or product_data.price is None or product_data.price < 0 or product_data.stock < 0:
            raise ValueError("Invalid product data")

        #check pre-existence of product 
        if self.product_repository.get_artisan_product_by_name(artisan_id, new_product.name):
            raise ValueError("Product with this name already exists for this artisan")
        try:
            saved_product = self.product_repository.create(new_product)
            print("Product saved successfully:")
            print(saved_product)
            print(saved_product.product_id)
            print(saved_product.category_id)
        except Exception as e:
            print(f"Error saving product: {e}")
            raise
        
        return ResponseRegisterProduct.from_domain_entities(saved_product, category)

