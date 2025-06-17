from tests.mocks.base import AbstractEntityFactory, FakerInstance
from tests.mocks.models import MockUserEntity, MockAddressEntity, MockArtisanEntity, MockBuyerEntity, MockProductEntity, MockCategoryEntity

fake = FakerInstance.get_instance()

class UserFactory(AbstractEntityFactory):
    def create(self, **kwargs):
        return MockUserEntity(**kwargs)
        
    def create_many(self, count, **kwargs):
        return [MockUserEntity(**kwargs) for _ in range(count)]


class AddressFactory(AbstractEntityFactory):
    def create(self, **kwargs):
        return MockAddressEntity(**kwargs)
        
    def create_many(self, count, **kwargs):
        return [MockAddressEntity(**kwargs) for _ in range(count)]


class ArtisanFactory(AbstractEntityFactory):
    def create(self, **kwargs):
        return MockArtisanEntity(**kwargs)
        
    def create_many(self, count, **kwargs):
        return [MockArtisanEntity(**kwargs) for _ in range(count)]


class BuyerFactory(AbstractEntityFactory):
    def create(self, **kwargs):
        return MockBuyerEntity(**kwargs)
        
    def create_many(self, count, **kwargs):
        return [MockBuyerEntity(**kwargs) for _ in range(count)]
    
class ProductFactory(AbstractEntityFactory):
    def create(self, **kwargs):
        return MockProductEntity(**kwargs)
        
    def create_many(self, count=1, **kwargs):
        return [MockProductEntity(**kwargs) for _ in range(count)]

class CategoryFactory(AbstractEntityFactory):
    def create(self, **kwargs):
        return MockCategoryEntity(**kwargs)
        
    def create_many(self, count=1, **kwargs):
        return [MockCategoryEntity(**kwargs) for _ in range(count)]

# Adicione à MockFactory
class MockFactory:
    def __init__(self):
        self.user = UserFactory()
        self.address = AddressFactory()
        self.artisan = ArtisanFactory()
        self.buyer = BuyerFactory()
        self.product = ProductFactory()
        self.category = CategoryFactory()