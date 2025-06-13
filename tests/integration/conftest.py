# script_teste_conexao.py
import os
import sys
import pytest
from dotenv import load_dotenv, find_dotenv

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
