from asyncio.log import logger
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
            logger.info("Product saved successfully:")
            logger.info(saved_product)
            logger.info(f"Product ID: {saved_product.product_id}")
            logger.info(f"Category ID: {saved_product.category_id}")
        except Exception as e:
            logger.error(f"Error saving product: {e}")
            raise
        
        return ResponseRegisterProduct.from_domain_entities(saved_product, category)
    
    def __get_categories_by_ids(self, category_ids: set[str]) -> list:
        """
        Helper method to fetch categories by their IDs.
        """
        categories = []
        for cat_id in category_ids:
            try:
                category = self.category_repository.get_by_id(cat_id)
            except Exception as e:
                logger.error(f"Error fetching category {cat_id}: {e}")
                category = None
                pass                         
            categories.append(category)
        return categories
    
    def get_all_products_by_artisan(self, artisan_id: str):
        try:
            artisan = self._artisan_repository.get_artisan_by_id(artisan_id)
            if not artisan:
                raise ValueError("Artisan not found")
            products = self.product_repository.find_by_artisan_id(artisan_id)
        except Exception as e:
            logger.error(f"Error fetching products for artisan {artisan_id}: {e}")
            raise
        
        if not products:
            logger.info(f"No products found for artisan {artisan_id}")
            return []
        
        # Fetch categories for the products
        category_ids = {product.category_id for product in products}
        categories = self.__get_categories_by_ids(category_ids)
        
        # Create a mapping of category_id to category
        category_map = {category.category_id: category for category in categories}
        
        # Map products to their respective categories
        return [
            ResponseRegisterProduct.from_domain_entities(product, category_map.get(product.category_id))
            for product in products
        ]
        