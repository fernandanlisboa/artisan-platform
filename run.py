# run.py
from app import create_app
import os

app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    # Executa a aplicação Flask, vinculando-a ao host '0.0.0.0' e à porta dinâmica.
    # 'debug=os.getenv('FLASK_DEBUG', 'True') == 'True'' mantém sua lógica de debug.
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'True') == 'True')

