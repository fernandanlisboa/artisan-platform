# script_teste_conexao.py
import os
import sys
import pytest
from dotenv import load_dotenv, find_dotenv
from tests.mocks.factories import MockFactory

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Carregue o arquivo .env.testing
env_file = find_dotenv('.env.testing')
load_dotenv(env_file, override=True)

# Defina o ambiente ANTES de importar a aplicação
os.environ['FLASK_ENV'] = 'testing'

# Agora importe a aplicação
import json
import uuid
from app import create_app, db

# Crie uma instância do MockFactory para ser usada em todos os testes de integração
mock_factory = MockFactory()

@pytest.fixture(scope="function", autouse=True)
def setup_buyer_test_db(app):
    """Configura banco para testes específicos do comprador."""
    with app.app_context():
        yield
        db.session.rollback()  # Rollback manual se necessário

@pytest.fixture(scope="session")
def app():
    """Fixture principal do aplicativo Flask para testes."""
    app = create_app('testing')
    print(f"\nCONFIRMAÇÃO: Usando banco {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"CONFIRMAÇÃO: TESTING={app.config['TESTING']}\n")
    return app

@pytest.fixture(scope="session", autouse=True)
def create_tables(app):
    """Cria todas as tabelas no banco de teste."""
    with app.app_context():
        db.create_all()
        print("Tabelas criadas no banco de teste")
    yield

@pytest.fixture(scope="session")
def client(app):
    """Retorna um cliente de teste Flask para fazer requisições."""
    return app.test_client()

@pytest.fixture(scope="function")
def session(app):
    """Fornece uma sessão de banco de dados para testes."""
    with app.app_context():
        # Cria um savepoint para rollback depois
        db.session.begin_nested()
        
        yield db.session
        
        # Rollback após o teste
        db.session.rollback()


@pytest.fixture
def created_address(session, valid_address_data): # Uma fixture pode usar outra!
    from app.infrastructure.persistence.models_db.address_db_model import AddressDBModel
    address = AddressDBModel(**valid_address_data)
    session.add(address)
    session.commit()
    return address

@pytest.fixture
def created_user(session, created_address, valid_user_data):
    from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
    # Garante que o ID do endereço na fixture de usuário seja o mesmo do endereço criado
    valid_user_data['address_id'] = created_address.address_id
    user = UserDBModel(**valid_user_data)
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def created_artisan(session, created_user, valid_artisan_data):
    from app.infrastructure.persistence.models_db.artisan_db_model import ArtisanDBModel
    valid_artisan_data['artisan_id'] = created_user.user_id
    artisan = ArtisanDBModel(**valid_artisan_data)
    session.add(artisan)
    session.commit()
    return artisan

@pytest.fixture
def created_category(session, valid_category_data):
    from app.infrastructure.persistence.models_db.category_db_model import CategoryDBModel
    category = CategoryDBModel.query.filter_by(name=valid_category_data['name']).first()
    if category is None:
        category = CategoryDBModel(**valid_category_data)
        session.add(category)
        session.commit()
    valid_category_data['category_id'] = category.category_id
    return category

@pytest.fixture
def mock_address_data():
    """Gera dados de endereço aleatórios usando o MockFactory."""
    address = mock_factory.address.create()
    return {
        "street": address.street,
        "number": address.number,
        "complement": address.complement,
        "neighborhood": address.neighborhood,
        "city": address.city,
        "state": address.state,
        "zip_code": address.zip_code,
        "country": address.country
    }

@pytest.fixture
def mock_buyer_data():
    """Gera dados de comprador aleatórios usando o MockFactory."""
    buyer = mock_factory.buyer.create()
    return {
        "full_name": buyer.full_name,
        "phone": buyer.phone,
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com",  # Email único
        "password": "ValidPassword123!"  # Senha padrão para testes
    }

@pytest.fixture
def mock_artisan_data():
    """Gera dados de artesão aleatórios usando o MockFactory."""
    artisan = mock_factory.artisan.create()
    return {
        "store_name": artisan.store_name,
        "phone": artisan.phone,
        "bio": artisan.bio,
        "email": f"artisan_{uuid.uuid4().hex[:8]}@example.com",
        "password": "ValidPassword123!"
    }

@pytest.fixture
def mock_product_data():
    """Gera dados de produto aleatórios usando o MockFactory."""
    product = mock_factory.product.create()
    return {
        'name': f"Test Product {uuid.uuid4().hex[:8]}",  # Nome único
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category_id': str(uuid.uuid4())
    }

@pytest.fixture
def mock_category_data():
    """Gera dados de categoria aleatórios usando o MockFactory."""
    category = mock_factory.category.create()
    return {
        'name': category.name,
        'description': category.description
    }
