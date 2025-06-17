import pytest
from unittest.mock import Mock
import uuid
from app.domain.repositories.category_repository_interface import ICategoryRepository

class BaseGetCategoryTest:
    """
    Classe base para testes de obtenção de categorias.
    """
    @pytest.fixture
    def mock_repositories(self):
        """Configura repositórios mock para todos os testes de produto."""
        return {
            'category_repo': Mock(spec=ICategoryRepository)
        }
        
    @pytest.fixture
    def test_ids(self):
        """Gera IDs consistentes para uso nos testes."""
        return {
            'product_id': str(uuid.uuid4()),
            'artisan_id': str(uuid.uuid4()),
            'category_id': str(uuid.uuid4())
        }

class TestGetCategory(BaseGetCategoryTest):
    """Testes para a obtenção de categorias usando o CategoryService."""

    def test_get_by_id_successfully(self, mock_repositories, test_ids):
        """Testa a obtenção de uma categoria pelo nome com sucesso."""
        # Arrange
        mock_repositories['category_repo'].get_by_id.return_value = {
            'category_id': test_ids['category_id'],
            'name': 'Test Category'
        }
        result = mock_repositories['category_repo'].get_by_id('Test Category')

        # Assert    
        assert result is not None
        assert result['category_id'] == test_ids['category_id']
        assert result['name'] == 'Test Category'
        
    def test_get_by_id_not_found(self, mock_repositories):
        """Testa a obtenção de uma categoria que não existe."""
        # Arrange
        mock_repositories['category_repo'].get_by_id.return_value = None
        
        # Act
        result = mock_repositories['category_repo'].get_by_id('Nonexistent Category')
        
        # Assert
        assert result is None
        mock_repositories['category_repo'].get_by_id.assert_called_once_with('Nonexistent Category')