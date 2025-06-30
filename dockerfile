# Usa uma imagem base oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Melhora o cache do pip
RUN pip install --upgrade pip

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta 8080, que é o padrão que o Cloud Run espera
EXPOSE 8080

# Comando para rodar a aplicação com Gunicorn (servidor de produção)
# - "--bind", "0.0.0.0:8080": Escuta em todas as interfaces na porta 8080. A variável $PORT é injetada pelo Cloud Run.
# - "run:app": Diz ao Gunicorn para encontrar o objeto 'app' no arquivo 'run.py'.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "run:app"]
