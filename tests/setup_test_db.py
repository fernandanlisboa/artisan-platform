# tests/setup_test_db.py
import os
import sys
import subprocess
from dotenv import load_dotenv, find_dotenv

def setup_test_database():
    """Configura o banco de dados de teste usando variáveis de ambiente temporárias."""
    # Adiciona o diretório raiz do projeto ao PYTHONPATH
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, project_root)
    
    # Carrega o ambiente de teste específico
    env_file = find_dotenv('.env.testing')
    load_dotenv(env_file, override=True)
    
    # Define explicitamente a variável de ambiente para teste
    os.environ['FLASK_ENV'] = 'testing'
    
    # Imprime as variáveis para debug
    test_db_url = os.environ.get('DATABASE_URL')
    print(f"Usando banco de teste: {test_db_url}")
    print(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")
    
    # Executa o upgrade do Alembic
    try:
        result = subprocess.run(['alembic', 'upgrade', 'head'], check=True)
        print("Migrações aplicadas com sucesso ao banco de teste!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar migrações: {e}")

# Executa quando chamado diretamente
if __name__ == "__main__":
    setup_test_database()