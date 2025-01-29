FROM python:3.11-slim

# Evitar prompts durante a instalação de pacotes
ENV DEBIAN_FRONTEND=noninteractive

# Definir diretório de trabalho
WORKDIR /app

# Adicionar diretório ao PYTHONPATH
ENV PYTHONPATH=/app:${PYTHONPATH}

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
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretório para relatórios
RUN mkdir -p /app/relatorios && chmod 777 /app/relatorios

# Copiar o código fonte
COPY . .

# Expor porta
EXPOSE 6248

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6248"]
