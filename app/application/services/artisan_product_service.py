from app.domain.repositories.product_repository_interface import IProductRepository

class ArtisanProductService:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def create_artisan_product(self, artisan_id, product_data):
        return self.product_repository.create_artisan_product(artisan_id, product_data)

