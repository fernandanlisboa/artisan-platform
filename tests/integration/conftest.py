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
    with app.app_context():
        db.drop_all() # <--- ESTA LINHA LIMPA O BANCO DE DADOS APÓS A SESSÃO DE TESTES
        print("Tabelas deletadas após a sessão de teste")

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
def created_product(session, created_artisan, created_category, valid_product_data):
    from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel
    # Garante que o ID da categoria na fixture de produto seja o mesmo da categoria criada
    valid_product_data['product_id'] = str(uuid.uuid4())  # Garante que o ID do produto seja único
    valid_product_data['category_id'] = created_category.category_id
    valid_product_data['artisan_id'] = created_artisan.artisan_id
    product = ProductDBModel.query.filter_by(product_id=valid_product_data['product_id']).first()
    if product is None:
        product = ProductDBModel(**valid_product_data)
        session.add(product)
        session.commit()
    return product

@pytest.fixture
def created_multiple_categories(session, valid_categories_data):
    from app.infrastructure.persistence.models_db.category_db_model import CategoryDBModel
    categories = []
    for data in valid_categories_data:
        category = CategoryDBModel.query.filter_by(name=data['name']).first()
        if category is not None:
            categories.append(category)
            continue
        category = CategoryDBModel(**data)
        session.add(category)
        session.commit()
        categories.append(category)
    return categories

@pytest.fixture
def created_multiple_products_same_category(session, created_artisan, created_multiple_categories, valid_products_data):
    from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel
    products = []
    for data in valid_products_data:
        data['category_id'] = created_multiple_categories[0].category_id
        data['artisan_id'] = created_artisan.artisan_id
        product = ProductDBModel.query.filter_by(product_id=data['product_id']).first()
        if product is not None:
            continue
        product = ProductDBModel(**data)
        session.add(product)
        session.commit()
        products.append(product)
    return products

@pytest.fixture
def created_multiple_products_different_categories(session, created_artisan, valid_categories_data, valid_products_data):
    from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel
    products = []
    for i, data in enumerate(valid_products_data):
        data['category_id'] = valid_categories_data[i]['category_id']
         # Garante que cada produto tenha um ID único
        data['artisan_id'] = created_artisan.artisan_id
        product = ProductDBModel.query.filter_by(product_id=data['product_id']).first()
        if product is not None:
            products.append(product)
            continue
        product = ProductDBModel(**data)
        session.add(product)
        session.commit()
        products.append(product)
    return products