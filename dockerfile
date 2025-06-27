# Dockerfile

# Usa uma imagem base oficial do Python (Python 3.9 é a versão que temos usado)
FROM python:3.12-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências e instala as dependências Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o Flask vai usar (padrão 5000)
EXPOSE 5000

# Define a variável de ambiente FLASK_APP para o Flask
ENV FLASK_APP=run.py
ENV FLASK_DEBUG=False

# Comando para rodar a aplicação Flask quando o contêiner iniciar
CMD ["flask", "run", "--host=0.0.0.0", "--port", "5000"]