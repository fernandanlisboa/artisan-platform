from collections import Counter
from decimal import Decimal
import uuid
import json
import pytest

from app.domain.models.category import CategoryEntity
from app.domain.models.product import ProductEntity
from app.infrastructure.persistence.category_repository import CategoryRepository
from app.infrastructure.persistence.product_repository import ProductRepository
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
    def valid_categories_data(self):
        mock_categories = mock_factory.category.create_many(2)
        return [
            {
                "category_id": mock_category.category_id,
                "name": mock_category.name,
                "description": mock_category.description
            } for mock_category in mock_categories
        ]
    
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
        
    @pytest.fixture
    def valid_products_data(self, test_ids):
        mock_products = mock_factory.product.create_many(2)
        return [
            {
                "product_id": product.product_id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "category_id": None,
                "artisan_id": test_ids['artisan_id'],
                "image_url": product.image_url
            } for product in mock_products
        ]
        
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

    def test_get_products_by_inexistent_artisan(self, client):
        invalid_artisan_id = str(uuid.uuid4())
        response = client.get(f"/api/artisan/{invalid_artisan_id}/products")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['message'] == "Artisan not found"

    def test_get_products_by_artisan_with_no_products(self, client, created_artisan):
        artisan_id = created_artisan.artisan_id
        response = client.get(f"/api/artisan/{artisan_id}/products")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0, "Expected no products for this artisan"
        
    def test_get_products_by_artisan_from_same_category(self, client, created_multiple_products_same_category, created_product):
        
        same_category_products = created_multiple_products_same_category
        artisan_id = same_category_products[0].artisan_id
        category_id = same_category_products[0].category_id
        product1 = same_category_products[0]
        product2 = same_category_products[1]
        product3 = created_product
        
        
        response = client.get(f"/api/artisan/{artisan_id}/products")
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert isinstance(data, list)
        assert len(data) >= 3, "Expected at least two products for this artisan"
        assert all(p['artisan_id'] == artisan_id for p in data), "Expected all products to belong to the same artisan"
        assert any(p['product_id'] == product1.product_id for p in data), "Expected product1 to be in the response"
        assert any(p['product_id'] == product2.product_id for p in data), "Expected product2 to be in the response"
        assert any(p['product_id'] == product3.product_id for p in data), "Expected product3 to be in the response"
        counter_cats = Counter(p['category']['category_id'] for p in data)
        assert counter_cats[product3.category_id] == 1, "Expected products to be from different categories"
        assert counter_cats[category_id] == 2, "Expected two products from the same category"
        
    def test_get_products_by_different_categories(self, client, created_multiple_products_same_category, created_product):
        #TODO: Implement this test to check if products from different categories are returned correctly
        pass