import os

# Define o ambiente para 'testing' ANTES de importar o create_app
# Isso garante que ele carregue a configuração correta
os.environ['FLASK_ENV'] = 'testing'

from app import create_app

# Cria a instância da aplicação no modo de teste
app = create_app('testing')

# O código mágico para listar as rotas
with app.app_context():
    print("-" * 80)
    print(f"{'Endpoint':<40} {'Methods':<20} {'URL Rule':<40}")
    print("-" * 80)
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        print(f"{rule.endpoint:<40} {methods:<20} {rule.rule:<40}")
    print("-" * 80)