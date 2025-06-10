# script_teste_conexao.py
import sqlalchemy
from dotenv import load_dotenv
import os

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