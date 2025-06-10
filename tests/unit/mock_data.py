from datetime import datetime
import uuid
from faker import Faker

fake = Faker()

# Classes de mock para entidades
class MockUserEntity:
    def __init__(self, user_id=None, email=None, password=None, status='active', address_id=None, registration_date=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.email = email or fake.email()
        self.password = password or fake.password()
        self.status = status
        self.address_id = address_id
        self.registration_date = registration_date or datetime.now()

class MockArtisanEntity:
    def __init__(self, artisan_id=None, store_name=None, phone=None, bio=None, status='active'):
        self.artisan_id = artisan_id or str(uuid.uuid4())
        self.store_name = store_name or fake.company()
        self.phone = phone or fake.phone_number()
        self.bio = bio or fake.text(max_nb_chars=200)
        self.status = status
class MockBuyerEntity:
    def __init__(self, buyer_id=None, full_name=None, phone=None, address=None):
        self.buyer_id = buyer_id or str(uuid.uuid4())
        self.full_name = full_name or fake.name()
        self.phone = phone or fake.phone_number()
        self.address = address

class MockAddressEntity:
    def __init__(self, address_id=None, street=None, number=None, complement=None, 
                neighborhood=None, city=None, state=None, zip_code=None, country=None):
        self.address_id = address_id or str(uuid.uuid4())
        self.street = street or fake.street_name()
        self.number = number or fake.building_number()
        self.complement = complement or fake.secondary_address()
        self.neighborhood = neighborhood or fake.city_suffix()
        self.city = city or fake.city()
        self.state = state or fake.state_abbr()
        self.zip_code = zip_code or fake.postcode()
        self.country = country or fake.country()

# A sua classe MockFactory
class MockFactory:
    @staticmethod
    def create_user(override_values=None):
        values = {
            'user_id': str(uuid.uuid4()),
            'email': fake.email(),
            'password': fake.password(),
            'status': 'active',
            'address_id': None
        }
        
        if override_values:
            values.update(override_values)
            
        return MockUserEntity(**values)
    
    @staticmethod
    def create_buyer(override_values=None):
        """Cria um MockBuyerEntity com valores aleatórios que podem ser sobrescritos"""
        values = {
            'buyer_id': str(uuid.uuid4()),
            'full_name': fake.name(),
            'phone': fake.phone_number(),
            'address': fake.street_address()
        }
        
        if override_values:
            values.update(override_values)
            
        return MockBuyerEntity(**values)
    
    @staticmethod
    def create_address(override_values=None):
        """Cria um MockAddressEntity com valores aleatórios que podem ser sobrescritos"""
        values = {
            'address_id': str(uuid.uuid4()),
            'street': fake.street_name(),
            'number': fake.building_number(),
            'complement': fake.secondary_address(),
            'neighborhood': fake.city_suffix(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.postcode(),
            'country': fake.country()
        }
        
        if override_values:
            values.update(override_values)
            
        return MockAddressEntity(**values)
    
    # create artisan method
    @staticmethod
    def create_artisan(override_values=None):
        """Cria um MockArtisanEntity com valores aleatórios que podem ser sobrescritos"""
        values = {
            'artisan_id': str(uuid.uuid4()),
            'store_name': fake.company(),
            'phone': fake.phone_number(),
            'bio': fake.text(max_nb_chars=200),
            'status': 'active'
        }
        
        if override_values:
            values.update(override_values)
            
        return MockArtisanEntity(**values)