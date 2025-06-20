import pytest
import uuid
from app.presentation.dtos.product_dtos import CategoryDTO
from tests.unit.products.base_product_test import mock_factory, BaseProductTest

class TestGetProductsByArtisan(BaseProductTest):
    """Testes para a obtenção de produtos usando o ProductService."""
    def create_base_products(self, mock_repositories, mock_factory, test_ids):
        """Cria produtos básicos para os testes."""  
        pass
    
    def test_get_all_products_successfully(self, service, mock_repositories, mock_entities, test_ids):
        """Testa a obtenção de todos os produtos."""
        # Arrange
        print(f"category: {mock_entities['category']}")
        print(mock_entities['artisan'])
        artisan_id_to_find = test_ids['artisan_id']
        category_id_for_product = test_ids['category_id']
        
        # O mock_entities['product'] já tem o artisan_id e category_id corretos
        product1 = mock_entities['product']
        
        # Configure o mock do product_repo para retornar esta lista
        mock_repositories['product_repo'].find_by_artisan_id.return_value = [product1]
        mock_repositories['category_repo'].get_by_id.return_value = mock_entities['category']
        # ACT
        # Chame o método correto no serviço: get_all_products_by_artisan
        products = service.get_all_products_by_artisan(artisan_id_to_find)
        
        # ASSERT
        assert products is not None
        assert isinstance(products, list)
        assert len(products) == 1
        assert products is not None
        assert isinstance(products, list)
        assert len(products) == 1
        
        # Verifica se o DTO de resposta está correto
        response_product = products[0]
        assert response_product.product_id == product1.product_id
        assert response_product.name == product1.name
        assert response_product.artisan_id == product1.artisan_id
        
        # Verifica a categoria aninhada
        assert response_product.category is not None
        assert isinstance(response_product.category, CategoryDTO)
        # --- CORREÇÃO AQUI: Acessa o atributo real do mock_entities['category'] ---
        assert response_product.category.category_id == mock_entities['category'].category_id
        assert response_product.category.name == mock_entities['category'].name # Verifica se a lista retornada é a esperada
        
        # Verifica se o método find_by_artisan_id do repositório foi chamado corretamente
        mock_repositories['product_repo'].find_by_artisan_id.assert_called_once_with(artisan_id_to_find)
        mock_repositories['category_repo'].get_by_id.assert_called_once_with(category_id_for_product) # Passa o ID real
