# app/__init__.py
from fastapi import FastAPI
from app.common.config import config_by_name
import os

def create_app(config_name=None):
    # Use o parâmetro se fornecido, senão use a variável de ambiente
    if config_name is None:
        config_name = os.getenv('API_ENV', 'development')
    
    # Carregar configuração
    config = config_by_name[config_name]
    
    # Criar app FastAPI
    app = FastAPI(
        title="Plataforma de Artesãos API",
        description="API para gerenciar artesãos, compradores e produtos.",
        version="1.0",
        docs_url="/swagger-ui",
        redoc_url="/redoc"
    )
    
    # Registrar routers
    from app.presentation.controllers.register_controller import register_router
    from app.presentation.controllers.auth_router import auth_router
    from app.presentation.controllers.artisan_controller import artisan_router
    
    app.include_router(register_router, prefix="/api")
    app.include_router(auth_router, prefix="/api")
    app.include_router(artisan_router, prefix="/api")
    
    # Middleware para segurança
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        
        # Remove/substitui informações de versão do servidor
        response.headers['Server'] = 'Artisan Platform'
        
        # Proteções adicionais contra XSS e outros ataques
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response
    
    return app