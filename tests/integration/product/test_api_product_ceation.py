import json
import pytest
import uuid
from tests.integration.conftest import mock_factory
from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel

class TestAPIProductCreation:
    @pytest.fixture
    def test_ids(self):
        return {
            "address_id": str(uuid.uuid4()),
            "artisan_id": str(uuid.uuid4()),
            "category_id": str(uuid.uuid4()),
            "product_id": str(uuid.uuid4())
        }

    @pytest.fixture
    def valid_address_data(self, test_ids):
        mock_address = mock_factory.address.create()
        return {
            "address_id": test_ids['address_id'],
            "street": mock_address.street,
            "number": mock_address.number,
            "complement": mock_address.complement,
            "neighborhood": mock_address.neighborhood,
            "city": mock_address.city,
            "state": mock_address.state,
            "zip_code": mock_address.zip_code,
            "country": mock_address.country
        }
    
    @pytest.fixture
    def valid_user_data(self, test_ids):
        mock_user = mock_factory.user.create()
        return {
            "user_id": test_ids["artisan_id"],
            "email": mock_user.email,
            "password_hash": mock_user.password,
            "address_id": test_ids['address_id']
        }
        
    @pytest.fixture
    def valid_artisan_data(self, test_ids):
        mock_artisan = mock_factory.artisan.create()
        return {
            "artisan_id": test_ids['artisan_id'],
            "store_name": mock_artisan.store_name,
            "phone": mock_artisan.phone,
            "bio": mock_artisan.bio
        }
        
    @pytest.fixture
    def valid_category_data(self, test_ids):
        mock_category = mock_factory.category.create()
        return {
            "category_id": test_ids['category_id'],
            "name": mock_category.name,
            "description": mock_category.description
        }
    
    @pytest.fixture
    def valid_product_data(self, test_ids):
        mock_product = mock_factory.product.create()
        return {
            "name": mock_product.name,
            "description": mock_product.description,
            "price": mock_product.price,
            "stock": mock_product.stock,
            "category_id": test_ids['category_id']
        }

    def test_create_product_successfully(self, app, session, client, created_artisan, created_category, valid_product_data):
        valid_product_data['category_id'] = created_category.category_id
        
        response = client.post(f'/api/artisan/{created_artisan.artisan_id}/product', data=json.dumps(valid_product_data), content_type='application/json')
        assert response.status_code == 201
        assert 'product_id' in response.json
        assert response.json['name'] == valid_product_data['name']
        assert response.json['price'] == valid_product_data['price']
        product = ProductDBModel.query.get(response.json['product_id'])
        assert product is not None

