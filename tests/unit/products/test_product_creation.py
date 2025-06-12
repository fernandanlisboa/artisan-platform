import pytest
from tests.unit.products.base_product_creation_test import BaseProductCreationTest

class TestProductCreation(BaseProductCreationTest):
    """Testes para a criação de produtos usando o ProductService."""

    @pytest.fixture
    def product_factory(self):
        """Retorna a factory de produtos do mock_factory."""
        return mock_factory.product
    
    def test_create_product_successfully(self, service, mock_repositories, valid_product_request, test_ids):
        """Testa a criação de um produto com sucesso pelo serviço."""
        # Arrange
        mock_repositories['artisan_repo'].get_by_id.return_value = mock_factory.artisan.create(
            artisan_id=test_ids['artisan_id']
        )
        mock_repositories['category_repo'].get_by_id.return_value = mock_factory.category.create(
            category_id=test_ids['category_id']
        )
        mock_repositories['product_repo'].create.return_value = mock_factory.product.create(
            product_id=test_ids['product_id'],
            **valid_product_request
        )
        
        # Act
        result = service.create_product(valid_product_request)
        
        # Assert
        assert result is not None
        assert result.product_id == test_ids['product_id']
        assert result.name == valid_product_request['name']
        
        # Verify repository calls
        mock_repositories['artisan_repo'].get_by_id.assert_called_once_with(valid_product_request['artisan_id'])
        mock_repositories['category_repo'].get_by_id.assert_called_once_with(valid_product_request['category_id'])
        mock_repositories['product_repo'].create.assert_called_once()
    
    def test_create_product_with_invalid_price(self, service, mock_repositories, valid_product_request):
        """Testa a criação de um produto com preço inválido."""
        # Arrange
        invalid_request = dict(valid_product_request)
        invalid_request['price'] = -10.0
        
        # Act & Assert
        with pytest.raises(ValueError):
            service.create_product(invalid_request)
    
    def test_create_product_with_missing_name(self, service, mock_repositories, valid_product_request):
        """Testa a criação de um produto sem nome."""
        # Arrange
        invalid_request = dict(valid_product_request)
        invalid_request['name'] = ""
        
        # Act & Assert
        with pytest.raises(ValueError):
            service.create_product(invalid_request)
    
    def test_create_product_with_invalid_category(self, service, mock_repositories, valid_product_request):
        """Testa a criação de um produto com categoria inválida."""
        # Arrange
        mock_repositories['category_repo'].get_by_id.return_value = None
        
            
    def test_create_product_with_nonexistent_artisan(self, service, mock_repositories, valid_product_request):
        """Testa a criação de um produto para um artesão que não existe."""
        # Arrange
        mock_repositories['artisan_repo'].get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError):
            service.create_product(valid_product_request)