# Imagem leve do Python
FROM python:3.9-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos locais para dentro do container
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Expõe a porta padrão do app
EXPOSE 8080

# Comando de execução do app com Gunicorn
CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "1"]
