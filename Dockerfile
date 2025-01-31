FROM python:3.11-slim

# Evitar prompts durante a instalação de pacotes
ENV DEBIAN_FRONTEND=noninteractive

# Definir diretório de trabalho
WORKDIR /app

# Adicionar diretório ao PYTHONPATH
ENV PYTHONPATH=/app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wkhtmltopdf \
    libfontconfig1 \
    libxrender1 \
    xfonts-base \
    xfonts-75dpi \
    fonts-liberation \
    # Dependências do WeasyPrint
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta que a aplicação usa
EXPOSE 6248

# Definir variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6248"]
