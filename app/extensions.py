from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()
api = Api(
    version='1.0',
    title='Plataforma de Artesãos API',
    description='API para gerenciar artesãos, compradores e produtos.',
    doc='/swagger-ui/'
)