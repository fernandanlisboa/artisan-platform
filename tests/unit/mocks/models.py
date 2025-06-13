import uuid
from datetime import datetime, timezone
from tests.unit.mocks.base import BaseMockEntity, FakerInstance
import random

fake = FakerInstance.get_instance()

class MockUserEntity(BaseMockEntity):
    def __init__(self, user_id=None, email=None, password=None, status='active', 
                 address_id=None, registration_date=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.email = email or fake.email()
        self.password = password or fake.password()
        self.status = status
        self.address_id = address_id
        self.registration_date = registration_date or datetime.now(timezone.utc)

class MockArtisanEntity(BaseMockEntity):
    def __init__(self, artisan_id=None, store_name=None, phone=None, bio=None, status='active'):
        self.artisan_id = artisan_id or str(uuid.uuid4())
        self.store_name = store_name or fake.company()
        self.phone = phone or fake.phone_number()
        self.bio = bio or fake.text(max_nb_chars=200)
        self.status = status

class MockBuyerEntity(BaseMockEntity):
    def __init__(self, buyer_id=None, full_name=None, phone=None, address=None):
        self.buyer_id = buyer_id or str(uuid.uuid4())
        self.full_name = full_name or fake.name()
        self.phone = phone or fake.phone_number()
        self.address = address

class MockAddressEntity(BaseMockEntity):
    def __init__(self, address_id=None, street=None, number=None, complement=None, 
                neighborhood=None, city=None, state=None, zip_code=None, country=None):
        self.address_id = address_id or str(uuid.uuid4())
        self.street = street or fake.street_name()
        self.number = number or str(fake.building_number())
        self.complement = complement or fake.bairro()
        self.neighborhood = neighborhood or fake.city_suffix()
        self.city = city or fake.city()
        self.state = state or fake.state_abbr()
        self.zip_code = zip_code or fake.postcode()
        self.country = country or fake.country()

class MockProductEntity(BaseMockEntity):
    def __init__(self, product_id=None, name=None, description=None, price=None,
                stock=None, artisan_id=None, category_id=None, 
                status='active', image=None, creation_date=None):
        self.product_id = product_id or str(uuid.uuid4())
        self.name = name or fake.color_name() + " " + fake.word().capitalize()
        self.description = description or fake.paragraph()
        self.price = price or round(random.uniform(10.0, 500.0), 2)
        self.stock = stock or random.randint(1, 100)
        self.artisan_id = artisan_id or str(uuid.uuid4())
        self.category_id = category_id or str(uuid.uuid4())
        self.status = status
        self.image_url = image or ''
        self.registration_date = creation_date or datetime.now(timezone.utc)
        
class MockCategoryEntity(BaseMockEntity):
    def __init__(self, category_id=None, name=None, description=None, parent_id=None):
        self.category_id = category_id or str(uuid.uuid4())
        self.name = name or fake.word().capitalize()
        self.description = description or fake.sentence()
        self.parent_id = parent_id