# tests/setup_test_db.py
import os
import subprocess
from dotenv import load_dotenv

def setup_test_database():
    """Configura o banco de dados de teste usando variáveis de ambiente temporárias."""
    load_dotenv()  # Carrega o .env
    
    # Guarda a configuração atual
    original_db_url = os.environ.get('DATABASE_URL')
    
    # Substitui temporariamente com a URL do banco de teste
    os.environ['DATABASE_URL'] = os.environ.get('TEST_DATABASE_URL')
    
    print(f"Usando banco de teste: {os.environ['DATABASE_URL']}")
    
    # Executa o upgrade do Alembic
    try:
        result = subprocess.run(['alembic', 'upgrade', 'head'], check=True)
        print("Migrações aplicadas com sucesso ao banco de teste!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar migrações: {e}")
    finally:
        # Restaura a configuração original
        if original_db_url:
            os.environ['DATABASE_URL'] = original_db_url

if __name__ == "__main__":
    setup_test_database()