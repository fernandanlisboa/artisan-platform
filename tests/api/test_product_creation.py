import pytest
import json
import uuid
from app.domain.models.artisan import ArtisanEntity
from app.domain.models.category import CategoryEntity
from app.infrastructure.persistence.artisan_repository import ArtisanRepository
from app.infrastructure.persistence.category_repository import CategoryRepository

class TestProductAPIIntegration:
    """Testes de integração para a API de produtos."""
    
    @pytest.fixture
    def valid_product_data(self):
        """Dados válidos para criação de produto via API."""
        from tests.integration.conftest import mock_factory
        
        product = mock_factory.product.create()
        return {
            'name': f"Test API Product {uuid.uuid4().hex[:8]}",  # Nome único
            'description': product.description,
            'price': float(product.price),  # Certifique-se de que é um float
            'stock': int(product.stock),    # Certifique-se de que é um int
            'category_id': None  # Será preenchido no teste
        }
    
    @pytest.fixture
    def test_artisan(self, app):
        """Cria um artesão de teste para uso nos testes."""
        from tests.integration.conftest import mock_factory
        
        with app.app_context():
            # Cria um registro de usuário e artesão primeiro
            artisan_repo = ArtisanRepository()
            
            # Verifica se já não existe um artesão de teste
            test_artisan_id = "test-artisan-" + uuid.uuid4().hex[:8]
            
            # Criar um artesão para o teste
            artisan = mock_factory.artisan.create(artisan_id=test_artisan_id)
            artisan_repo.create(artisan)
            
            return artisan
    
    @pytest.fixture
    def test_category(self, app):
        """Cria uma categoria de teste para uso nos testes."""
        from tests.integration.conftest import mock_factory
        
        with app.app_context():
            category_repo = CategoryRepository()
            
            # Criar uma categoria para o teste
            test_category_id = "test-category-" + uuid.uuid4().hex[:8]
            category = mock_factory.category.create(category_id=test_category_id)
            category_repo.create(category)
            
            return category
    
    def test_create_product_api_success(self, client, app, valid_product_data, test_artisan, test_category):
        """Testa a criação bem-sucedida de produto via API."""
        # Arrange - Usa os fixtures para artesão e categoria
        artisan_id = test_artisan.artisan_id
        valid_product_data['category_id'] = test_category.category_id
        
        # Act - Faz a requisição para a API
        response = client.post(
            f'/api/artisans/{artisan_id}/products',
            json=valid_product_data,
            content_type='application/json'
        )
        
        # Assert
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'product_id' in data
        assert data['name'] == valid_product_data['name']
        
        # Verifique se o produto foi realmente criado no banco
        with app.app_context():
            from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel
            saved_product = ProductDBModel.query.filter_by(name=valid_product_data['name']).first()
            assert saved_product is not None
            assert saved_product.artisan_id == artisan_id