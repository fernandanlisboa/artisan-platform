import os

# Definir ambiente antes de importar a aplicação
os.environ['API_ENV'] = 'testing'

from app import create_app

# Criar aplicação FastAPI
app = create_app('testing')

# Listar rotas (versão FastAPI)
print("-" * 80)
print(f"{'Endpoint':<40} {'Methods':<20} {'URL Path':<40}")
print("-" * 80)

# No FastAPI, as rotas são armazenadas em app.routes
for route in app.routes:
    methods = ','.join(route.methods) if hasattr(route, "methods") and route.methods else "N/A"
    path = route.path
    name = route.name or "unnamed"
    print(f"{name:<40} {methods:<20} {path:<40}")

print("-" * 80)