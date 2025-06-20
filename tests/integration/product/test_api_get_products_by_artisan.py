from decimal import Decimal
import uuid
import json
import pytest

from tests.integration.conftest import mock_factory

class TestAPIGetProductsByArtisan:
    #TODO: refatorar para ter uma classe base construindo os objetos necessários para os testes de produtos!

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
        
    def test_get_products_by_artisan_successfully(self, client, created_product):
        artisan_id = created_product.artisan_id
        product = created_product
        response = client.get(f"/api/artisan/{artisan_id}/products")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        for product_response in data:
            assert product.product_id == product_response['product_id'], f"Expected product_id {product.product_id}, got {product_response.product_id}"
            assert product.name == product_response['name'], f"Expected name {product.name}, got {product_response.name}"
            assert product.description == product_response['description'], f"Expected description {product.description}, got {product_response.description}"
            assert product.price == Decimal(str(product_response['price'])), f"Expected price {product.price}, got {product_response.price}"
            assert product.stock == product_response['stock'], f"Expected stock {product.stock}, got {product_response.stock}"
            assert product.category_id == product_response['category']['category_id'], f"Expected category_id {product.category_id}, got {product_response.category_id}"
            assert product.artisan_id == product_response['artisan_id'], f"Expected artisan_id {product.artisan_id}, got {product_response.artisan_id}"
