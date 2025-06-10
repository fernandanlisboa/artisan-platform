# script_teste_conexao.py
import sqlalchemy
from dotenv import load_dotenv
import os
import pytest
import json
import uuid
from app import create_app, db
from app.infrastructure.persistence.models_db.user_db_model import UserDBModel
from app.infrastructure.persistence.models_db.buyer_db_model import BuyerDBModel
from app.infrastructure.persistence.models_db.address_db_model import AddressDBModel

load_dotenv()

# Adapte para seu dialeto e variáveis
url = os.getenv("LOCAL_DATABASE_URL")
print(f"Tentando conectar com: {url}")

try:
    engine = sqlalchemy.create_engine(url)
    with engine.connect() as connection:
        print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Falha na conexão: {e}")

@pytest.fixture(scope="function", autouse=True)
def setup_buyer_test_db(app):  # REMOVA o parâmetro 'session'
    """Configura banco para testes específicos do comprador."""
    # Esta fixture será executada automaticamente antes de cada teste neste diretório
    
    with app.app_context():
        # Qualquer setup específico pode ser feito aqui
        yield
        
        # Cleanup após o teste
        db.session.rollback()  # Rollback manual se necessário

# Em conftest.py:
@pytest.fixture(scope="session")
def app():
    # Defina a variável de ambiente aqui
    os.environ['FLASK_ENV'] = 'testing'
    
    # Chame create_app() sem argumentos
    return create_app()

@pytest.fixture(scope="function")
def session(app):
    """Fornece uma sessão de banco de dados para testes."""
    with app.app_context():
        # Cria um savepoint para rollback depois
        db.session.begin_nested()
        
        yield db.session
        
        # Rollback após o teste
        db.session.rollback()

@pytest.fixture(scope="session")
def client(app):
    """Retorna um cliente de teste Flask para fazer requisições."""
    return app.test_client()
