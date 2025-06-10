import pytest
from alembic.config import Config as AlembicConfig
from alembic import command
from app import create_app, db as _db  

@pytest.fixture(scope='session')
def app():
    """
    Cria uma instância da aplicação Flask para toda a sessão de testes.
    Usa a configuração 'testing' do seu config.py.
    """
    return create_app('testing')  # Garanta que você tenha uma 'TestingConfig' no seu config.py

@pytest.fixture(scope='session')
def db(app):
    """
    Fixture de sessão para configurar o banco de dados UMA ÚNICA VEZ por execução do pytest.
    Isto resolve o seu pedido de "criar se não tiver criado" de forma eficiente.
    """
    with app.app_context():
        # Usa a abordagem correta do Alembic para criar o esquema do banco
        alembic_cfg = AlembicConfig("migrations/alembic.ini")
        alembic_cfg.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])
        command.upgrade(alembic_cfg, 'head')

        print("\nBanco de dados de teste criado e migrações aplicadas UMA VEZ.")
        
        # Passa o controle para os testes
        yield _db

        # Limpeza no final de TODA a sessão de testes
        _db.session.remove()
        _db.drop_all()
        print("\nBanco de dados de teste derrubado.")

@pytest.fixture(scope='function')
def session(db):
    """
    Fixture de função para fornecer uma sessão de banco de dados limpa para CADA teste.
    Isto garante que um teste não interfira no outro.
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    
    session = db.create_scoped_session(options={'bind': connection, 'binds': {}})
    db.session = session

    yield session

    # Limpeza após CADA teste
    session.remove()
    transaction.rollback()  # Desfaz todas as alterações do teste
    connection.close()

@pytest.fixture(scope='function')
def client(app):
    """Fixture para o cliente de teste do Flask."""
    return app.test_client()