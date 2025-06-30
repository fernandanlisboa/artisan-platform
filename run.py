# run.py
from app import create_app
import os

# O Gunicorn vai procurar por esta variável 'app' por padrão.
app = create_app()

# O bloco abaixo agora será usado apenas para desenvolvimento local
# e será ignorado pelo Gunicorn no contêiner.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)