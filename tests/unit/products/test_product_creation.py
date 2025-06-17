import pytest
# Importar apenas a classe BaseProductCreationTest
from app.presentation.dtos.product_dtos import RegisterProductRequest
from tests.unit.products.base_product_creation_test import BaseProductCreationTest

# mock_factory já é acessível dentro da classe pois é definido no módulo importado
class TestProductCreation(BaseProductCreationTest):
    """Testes para a criação de produtos usando o ProductService."""

    @pytest.fixture
    def product_factory(self):
        """Retorna a factory de produtos do mock_factory."""
        # A variável mock_factory já está acessível no escopo do módulo
        from tests.unit.products.base_product_creation_test import mock_factory
        return mock_factory.product
    
    def test_repo_create_product_successfully(self, mock_repositories, valid_product_request, test_ids):
        """Testa a criação de um produto com sucesso pelo repositorio."""
        # Arrange
        from tests.unit.products.base_product_creation_test import mock_factory
        mock_repositories['artisan_repo'].get_artisan_by_id.return_value = (
            mock_factory.artisan.create(
                artisan_id=test_ids['artisan_id']
            )
        )
        mock_repositories['category_repo'].get_by_id.return_value = (
            mock_factory.category.create(
                category_id=test_ids['category_id']
            )
        )
        artisan_id, data = valid_product_request
        data = {"artisan_id": artisan_id, **data}
        result = mock_repositories['product_repo'].create.return_value = (
            mock_factory.product.create(
                product_id=test_ids['product_id'],
                **data
            )
        )
        
        # Assert
        assert result is not None
        assert result.product_id == test_ids['product_id']
        assert result.name == valid_product_request[1]['name']
    
    def test_service_create_product_successfully(self, service, mock_repositories, valid_product_request, test_ids):
        """Testa a criação de um produto com sucesso pelo serviço."""
        # Arrange
        from tests.unit.products.base_product_creation_test import mock_factory
        mock_repositories['artisan_repo'].get_artisan_by_id.return_value = (
            mock_factory.artisan.create(
                artisan_id=test_ids['artisan_id']
            )
        )
        mock_repositories['category_repo'].get_by_id.return_value = (
            mock_factory.category.create(
                category_id=test_ids['category_id']
            )
        )
        artisan_id, data = valid_product_request
        request = {"artisan_id": artisan_id, **data}
        result = mock_repositories['product_repo'].create.return_value = (
            mock_factory.product.create(
                product_id=test_ids['product_id'],
                **request
            )
        )
        # Mock get_artisan_product_by_name to simulate no existing product with the same name
        mock_repositories['product_repo'].get_artisan_product_by_name.return_value = None
        request = RegisterProductRequest(**data)
        # Act
        result = service.create_artisan_product(artisan_id, request)
        
        # Assert
        assert result is not None
        assert result.product_id == test_ids['product_id']
        assert result.name == valid_product_request[1]['name']
        
        # Verify repository calls
        mock_repositories['artisan_repo'].get_artisan_by_id.assert_called_once_with(valid_product_request[0])
        mock_repositories['category_repo'].get_by_id.assert_called_once_with(test_ids['category_id'])
        mock_repositories['product_repo'].create.assert_called_once()
    
    def test_create_product_with_invalid_price(self, service, mock_repositories, valid_product_request):
        """Testa a criação de um produto com preço inválido."""
        # Arrange
        artisan_id, invalid_request = valid_product_request
        invalid_request['price'] = -10.0
        
        request = RegisterProductRequest(**invalid_request)
        with pytest.raises(ValueError):
            service.create_artisan_product(artisan_id, request)
    
    def test_create_product_with_missing_name(self, service, mock_repositories, valid_product_request):
        """Testa a criação de um produto sem nome."""
        # Arrange
        artisan_id, invalid_request = valid_product_request
        invalid_request['name'] = ""
        request = RegisterProductRequest(**invalid_request)
        with pytest.raises(ValueError):
            service.create_artisan_product(artisan_id, request)
    
    def test_create_product_with_invalid_category(self, service, mock_repositories, valid_product_request):
        """Testa a criação de um produto com categoria inválida."""
        # Arrange
        mock_repositories['category_repo'].get_by_id.return_value = None
        
        artisan_id, product_data = valid_product_request
        
        request = RegisterProductRequest(**product_data)
        with pytest.raises(ValueError):
            service.create_artisan_product(artisan_id, request)
            
    def test_create_product_with_nonexistent_artisan(self, service, mock_repositories, valid_product_request):
        """Testa a criação de um produto para um artesão que não existe."""
        # Arrange
        mock_repositories['category_repo'].get_by_id.return_value = None
        artisan_id, product_data = valid_product_request
        
        request = RegisterProductRequest(**product_data)
        with pytest.raises(ValueError):
            service.create_artisan_product(artisan_id, request)