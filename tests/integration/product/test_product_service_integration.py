import pytest
import uuid
from app import db
from app.application.services.artisan_product_service import ArtisanProductService
from app.infrastructure.persistence.product_repository import ProductRepository
from app.infrastructure.persistence.category_repository import CategoryRepository
from app.infrastructure.persistence.artisan_repository import ArtisanRepository
from app.presentation.dtos.product_dtos import RegisterProductRequest, ResponseRegisterProduct
from tests.integration.conftest import mock_factory
# --- FIXTURES ---

@pytest.fixture
def repositories(app):
    """Inicializa os repositórios reais, não mocks."""
    with app.app_context():
        return {
            'product_repo': ProductRepository(),
            'category_repo': CategoryRepository(),
            'artisan_repo': ArtisanRepository()
        }

@pytest.fixture
def service(repositories):
    """Cria o serviço de produto com repositórios reais."""
    return ArtisanProductService(
        product_repository=repositories['product_repo'],
        category_repository=repositories['category_repo'],
        artisan_repository=repositories['artisan_repo']
    )

@pytest.fixture
def valid_product_data():
    """Cria dados válidos para um produto usando o mock_factory."""
    from tests.integration.conftest import mock_factory
    
    product = mock_factory.product.create()
    return {
        'name': f"Test Product {uuid.uuid4().hex[:8]}",  # Nome único
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category_id': None  # Será preenchido no teste
    }

@pytest.fixture(autouse=True)
def clean_database(app):
    """Limpa o banco de dados de produtos antes de cada teste."""
    with app.app_context():
        try:
            # Limpar tabelas relevantes
            from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel
            ProductDBModel.query.delete()
            db.session.commit()
            print("Banco de dados de produtos limpo com sucesso")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao limpar banco de produtos: {e}")
        
        yield

class TestProductServiceIntegration:
    """
    Testes de integração para o serviço de produtos.
    Estes testes verificam se o serviço interage corretamente com o banco de dados real.
    """
    
    def test_create_product_via_service(self, service, repositories, valid_product_data, app):
        """Testa a criação de produto através do serviço diretamente."""
        with app.app_context():
            # Arrange - Primeiro precisamos garantir que há um artesão e uma categoria
            from app.domain.models.artisan import ArtisanEntity
            from app.domain.models.category import CategoryEntity
            from app.infrastructure.persistence.models_db.artisan_db_model import ArtisanDBModel
            from app.infrastructure.persistence.models_db.category_db_model import CategoryDBModel
            
            # Cria um artesão para o teste se não existir
            artisan_id = str(uuid.uuid4())
            if not ArtisanDBModel.query.filter_by(artisan_id=artisan_id).first():
                artisan = mock_factory.artisan.create(artisan_id=artisan_id)
                repositories['artisan_repo'].create(artisan)
            
            # Cria uma categoria para o teste se não existir
            category_id = str(uuid.uuid4())
            if not CategoryDBModel.query.filter_by(category_id=category_id).first():
                category = mock_factory.category.create(category_id=category_id)
                repositories['category_repo'].create(category)
            
            # Atualiza os dados do produto com os IDs criados
            valid_product_data['category_id'] = category_id
            
            # Act - Cria o produto
            request = RegisterProductRequest(**valid_product_data)
            result = service.create_artisan_product(artisan_id, request)
            
            # Assert - Verifica o resultado
            assert result is not None
            assert result.name == valid_product_data['name']
            assert result.description == valid_product_data['description']
            assert result.price == valid_product_data['price']
            
            # Assert - Verifica persistência no banco
            from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel
            saved_product = ProductDBModel.query.filter_by(name=valid_product_data['name']).first()
            assert saved_product is not None
            assert saved_product.description == valid_product_data['description']
            assert saved_product.artisan_id == artisan_id
    
    def test_duplicate_product_name_validation(self, service, repositories, valid_product_data, app):
        """Testa a validação de produto com mesmo nome para o mesmo artesão."""
        with app.app_context():
            # Arrange - Cria um produto primeiro
            artisan_id = str(uuid.uuid4())
            category_id = str(uuid.uuid4())
            
            # Configurações iniciais como no primeiro teste
            # [código para configurar artesão e categoria]
            
            # Primeiro produto
            first_request = RegisterProductRequest(**valid_product_data)
            service.create_artisan_product(artisan_id, first_request)
            
            # Act & Assert - Tenta criar produto com mesmo nome
            second_request = RegisterProductRequest(**valid_product_data)  # Mesmo nome
            with pytest.raises(ValueError) as excinfo:
                service.create_artisan_product(artisan_id, second_request)
            
            assert "Product with this name already exists" in str(excinfo.value)
    
    def test_create_product_nonexistent_category(self, service, valid_product_data, app):
        """Testa a criação de produto com categoria inexistente."""
        with app.app_context():
            # Arrange
            artisan_id = str(uuid.uuid4())
            # Configura uma categoria que não existe
            valid_product_data['category_id'] = str(uuid.uuid4())
            
            # Act & Assert
            request = RegisterProductRequest(**valid_product_data)
            with pytest.raises(ValueError) as excinfo:
                service.create_artisan_product(artisan_id, request)
            
            assert "Category not found" in str(excinfo.value)
    
    def test_create_product_nonexistent_artisan(self, service, repositories, valid_product_data, app):
        """Testa a criação de produto com artesão inexistente."""
        with app.app_context():
            # Arrange - Configure categoria existente
            category_id = str(uuid.uuid4())
            # [código para configurar categoria]
            
            valid_product_data['category_id'] = category_id
            
            # Act & Assert - Use um ID de artesão que não existe
            nonexistent_artisan_id = str(uuid.uuid4())
            request = RegisterProductRequest(**valid_product_data)
            with pytest.raises(ValueError) as excinfo:
                service.create_artisan_product(nonexistent_artisan_id, request)
            
            assert "Artisan not found" in str(excinfo.value)