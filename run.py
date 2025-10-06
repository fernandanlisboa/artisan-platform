# run.py
import uvicorn
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar banco de dados ANTES de criar a aplicação
db_url = os.getenv("DATABASE_URL")

# Setup database
from app.extensions import setup_db
db_config = setup_db(db_url)

# Only import models after DB setup
from app.infrastructure.persistence.models_db import *

# Criar aplicação DEPOIS de configurar o banco
from app import create_app
app = create_app()

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)