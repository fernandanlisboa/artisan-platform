import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    """Configuração base, com valores padrão."""
    # Chave secreta para segurança da sessão e outros recursos do Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'uma-chave-secreta-padrao-para-emergencias')
    
    # Configurações do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações do Flask
    JSON_AS_ASCII = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuração para o ambiente de desenvolvimento local."""
    DEBUG = True
    # Lê a URL do banco de dados do seu arquivo .env local
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    print("dev env")
    print(SQLALCHEMY_DATABASE_URI)

class TestingConfig(Config):
    """Configuração para o ambiente de testes (usado pelo CI/CD)."""
    TESTING = True
    # Lê a URL do banco de dados que o GitHub Actions cria e coloca no .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # Pode desativar a verificação de DB no startup durante os testes para agilizar
    CHECK_DB_CONNECTION_ON_STARTUP = 'False' 

class ProductionConfig(Config):
    """Configuração para o ambiente de produção (nuvem)."""
    # A URL do banco será injetada como variável de ambiente pela plataforma de nuvem
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # Força a verificação da conexão com o banco no startup de produção
    CHECK_DB_CONNECTION_ON_STARTUP = 'True'

# Dicionário que mapeia o nome do ambiente (string) para a classe de configuração
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}