FROM ubuntu:22.04

# Evitar prompts durante a instalação de pacotes
ENV DEBIAN_FRONTEND=noninteractive

# Definir diretório de trabalho
WORKDIR /app

# Instalar Python e outras dependências
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    build-essential \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Criar link simbólico para python3
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependências Python
RUN pip install -r requirements.txt

# Criar diretório para relatórios
RUN mkdir -p /app/relatorios && chmod 777 /app/relatorios

# Copiar o código fonte
COPY . .

# Expor porta
EXPOSE 6248

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6248"]
