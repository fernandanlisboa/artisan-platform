import os
from datetime import timedelta


class Config:
    """Configuração base, com valores padrão."""
    # Chave secreta para segurança da sessão e outros recursos
    SECRET_KEY = os.getenv('API_SECRET_KEY', 'uma-chave-secreta-padrao-para-emergencias')
    
    # Configurações do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações do Flask
    JSON_AS_ASCII = False
    DEBUG = False
    TESTING = False
    
    # JWT Configuration - ADICIONADO
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'fallback-secret-key-change-in-production'
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM') or 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES') or 30)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRE_DAYS') or 7)


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
    
    # Usa SQLite em memória em ambientes CI, ou MySQL localmente
    if os.getenv('CI') == 'true':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    
    print("teste env")
    print(SQLALCHEMY_DATABASE_URI)
    CHECK_DB_CONNECTION_ON_STARTUP = 'False'
    
    # JWT Configuration for testing - ADICIONADO
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'secret'
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM') or 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES') or 30)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRE_DAYS') or 7)



class ProductionConfig(Config):
    """Configuração para o ambiente de produção."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # JWT Configuration for production - OVERRIDE para valores seguros
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # DEVE ser definido em produção
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY must be set in production environment")


# Mapeamento dos ambientes
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
