import pytest
from unittest.mock import Mock
import uuid
from app.application.services.artisan_product_service import ArtisanProductService
from app.domain.repositories.product_repository_interface import IProductRepository
from app.domain.repositories.category_repository_interface import ICategoryRepository
from app.domain.repositories.artisan_repository_interface import IArtisanRepository
from tests.unit.mocks.factories import MockFactory

# Instanciando a factory no nível do módulo
mock_factory = MockFactory()

class BaseProductCreationTest:
    """
    Classe base para testes de criação de produtos.
    """
    
    @pytest.fixture
    def mock_repositories(self):
        """Configura repositórios mock para todos os testes de produto."""
        return {
            'product_repo': Mock(spec=IProductRepository),
            'category_repo': Mock(spec=ICategoryRepository),
            'artisan_repo': Mock(spec=IArtisanRepository)
        }
    
    @pytest.fixture
    def service(self, mock_repositories):
        """Cria o serviço de produto com repositórios mockados."""
        return ArtisanProductService(
            product_repository=mock_repositories['product_repo'],
            category_repository=mock_repositories['category_repo'],
            artisan_repository=mock_repositories['artisan_repo']
        )
    
    @pytest.fixture
    def test_ids(self):
        """Gera IDs consistentes para uso nos testes."""
        return {
            'product_id': str(uuid.uuid4()),
            'artisan_id': str(uuid.uuid4()),
            'category_id': str(uuid.uuid4())
        }
    
    @pytest.fixture
    def mock_entities(self, test_ids):
        """Usa a MockFactory para criar entidades de teste."""
        return {
            'product': mock_factory.product.create(
                product_id=test_ids['product_id'],
                artisan_id=test_ids['artisan_id'],
                category_id=test_ids['category_id']
            ),
            'artisan': mock_factory.artisan.create(
                artisan_id=test_ids['artisan_id']
            ),
            'category': mock_factory.category.create(
                category_id=test_ids['category_id']
            ) if hasattr(mock_factory, 'category') else None
        }
    
    @pytest.fixture
    def valid_product_request(self, test_ids):
        """Cria uma requisição de produto válida para testes."""
        product = mock_factory.product.create()
        return test_ids['artisan_id'], {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'category_id': test_ids['category_id'],
            # 'images': []  # URLs de imagens, se necessário
        }

