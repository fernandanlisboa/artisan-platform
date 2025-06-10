# app/__init__.py
from flask import Flask
import os
from app.extensions import db, api
from app.common.config import config_by_name # <--- Importa o dicionário de configurações

def create_app():
    # Determina qual ambiente usar. Padrão é 'development' se não for especificado.
    # O CI/CD irá definir FLASK_ENV=testing no arquivo .env.
    config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    
    # 1. CARREGA TODA A CONFIGURAÇÃO A PARTIR DO OBJETO CORRETO
    app.config.from_object(config_by_name[config_name])

    # 2. INICIALIZA AS EXTENSÕES COM O APP JÁ CONFIGURADO
    db.init_app(app)
    api.init_app(app)

    # 3. VERIFICA A CONEXÃO COM O BANCO (seu código de verificação)
    # Este bloco continua útil, especialmente para debugar o startup em produção
    with app.app_context():
        if app.config.get('CHECK_DB_CONNECTION_ON_STARTUP', 'False') == 'True':
            # ... seu código de verificação de conexão ...
            print("INFO: Verificação de conexão com DB ativada.")
            pass # Mantenha sua lógica aqui

    # 4. REGISTRA OS NAMESPACES DA API
    from app.presentation.controllers.auth_controller import auth_ns 
    api.add_namespace(auth_ns) 

    # Adicionar middleware de segurança para todas as respostas
    @app.after_request
    def add_security_headers(response):
        # Remove/substitui informações de versão do servidor
        response.headers['Server'] = 'Artisan Platform'
        
        # Configuração de Content Security Policy
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; object-src 'none';"
        
        # Configuração de Permissions Policy
        response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=(), payment=()"
        
        # Proteções adicionais contra XSS e outros ataques
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response

    return app