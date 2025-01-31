# AI Geologia - Assistente Virtual para Relatórios Geológicos

Este projeto implementa um assistente virtual especializado em geologia que recebe mensagens via WhatsApp (texto ou áudio) e gera relatórios geológicos detalhados em formato PDF.

## Funcionalidades

- Recebimento de mensagens via WhatsApp (texto e áudio)
- Transcrição automática de mensagens de áudio usando IA
- Geração de relatórios geológicos usando LLMs (Large Language Models)
- Envio automático dos relatórios em PDF via WhatsApp
- API RESTful para integração com outros sistemas

## Pré-requisitos

- Docker e Docker Compose
- Chaves de API:
  - EVOLUTION_INSTANCE_TOKEN (para WhatsApp)
  - OPENAI_API_KEY (para LLM)
  - GROQ_API_KEY (para transcrição de áudio)

## Configuração

1. Clone o repositório:
```bash
git clone <repository-url>
cd ai_geologia
```

2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
EVOLUTION_INSTANCE_TOKEN=seu_token_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
GROQ_API_KEY=sua_chave_groq_aqui
```

## Executando com Docker

1. Construa e inicie os containers:
```bash
docker compose up -d --build
```

2. Verifique se o serviço está rodando:
```bash
docker compose ps
```

O serviço estará disponível em `http://localhost:6248`

## Testando

O projeto inclui scripts de teste na pasta `test-requests/` para validar diferentes funcionalidades:

### Teste de Mensagem de Texto

Para testar o processamento de mensagens de texto:
```bash
docker exec CONTAINER_ID python3 test-requests/test-text.py
```

### Teste de Mensagem de Áudio

Para testar o processamento de mensagens de áudio:
```bash
docker exec CONTAINER_ID python3 test-requests/test_transcribe.py
```

### Teste do Webhook

Para testar a integração completa via webhook:
```bash
docker exec CONTAINER_ID python3 test-requests/test_webhook.py
```

## Remover docker images

```bash
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
```

## Estrutura do Projeto

- `main.py`: Aplicação principal FastAPI
- `crew/`: Implementação do assistente usando CrewAI
- `test-requests/`: Scripts de teste
- `example-request/`: JSONs de exemplo para testes
- `transcribe_audio.py`: Módulo de transcrição de áudio
- `message_whatsapp.py`: Processamento de mensagens do WhatsApp
- `send_whatsapp.py`: Envio de mensagens via WhatsApp

## Endpoints da API

### POST /webhook
Endpoint principal que recebe as mensagens do WhatsApp.

Exemplo de requisição:
```json
{
  "event": "messages.upsert",
  "data": {
    "key": {
      "remoteJid": "5583XXXXXXXX@s.whatsapp.net"
    },
    "message": {
      "conversation": "Gerar relatório para terreno...."
    }
  }
}
```

## Desenvolvimento

Para desenvolvimento local sem Docker:

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o servidor:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 6248
```

## Contribuindo

1. Clone o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

# Rodando com Docker

## Desenvolvimento Local

### 1. Criar rede Docker
```bash
docker network create ai_geologia_network
```

### 2. Construir as imagens
```bash
# Build da imagem da aplicação
docker build -t ai_geologia .

# Build da imagem do Nginx (desenvolvimento)
cd nginx
docker build -t ai_geologia_nginx .
cd ..
```

### 3. Rodar os containers
```bash
# Rodar a aplicação
docker run -d \
  --name ai_geologia \
  --network ai_geologia_network \
  -v $(pwd)/relatorios:/app/relatorios \
  ai_geologia

# Rodar o Nginx
docker run -d \
  --name ai_geologia_nginx \
  --network ai_geologia_network \
  -p 80:80 \
  ai_geologia_nginx
```

### 4. Testar a API
```bash
# Teste básico
curl http://localhost/

# Teste do webhook
curl http://localhost/webhook
```

### 5. Comandos úteis para desenvolvimento
```bash
# Ver logs da aplicação
docker logs ai_geologia

# Ver logs do Nginx
docker logs ai_geologia_nginx

# Parar os containers
docker stop ai_geologia ai_geologia_nginx

# Remover os containers
docker rm ai_geologia ai_geologia_nginx
```

## Produção

### 1. Pré-requisitos
- Ter um domínio configurado apontando para o servidor
- Ter o Docker instalado no servidor
- Ter acesso SSH ao servidor

### 2. Configurar SSL
```bash
# No servidor
sudo apt-get update
sudo apt-get install certbot
sudo certbot certonly --standalone -d seu-dominio.com
```

### 3. Preparar arquivos de configuração
```bash
# No servidor
cd nginx
# Copiar configuração de produção
cp default.prod.conf default.conf
# Ajustar o domínio no arquivo
sed -i 's/seu-dominio.com/seu-dominio-real.com/g' default.conf
```

### 4. Construir as imagens
```bash
# Build da imagem da aplicação
docker build -t ai_geologia .

# Build da imagem do Nginx (produção)
cd nginx
docker build -t ai_geologia_nginx .
cd ..
```

### 5. Criar rede Docker
```bash
docker network create ai_geologia_network
```

### 6. Rodar em produção
```bash
# Rodar a aplicação
docker run -d \
  --name ai_geologia \
  --network ai_geologia_network \
  -v /path/to/relatorios:/app/relatorios \
  --restart unless-stopped \
  ai_geologia

# Rodar o Nginx com SSL
docker run -d \
  --name ai_geologia_nginx \
  --network ai_geologia_network \
  -p 80:80 \
  -p 443:443 \
  -v /etc/letsencrypt/live/seu-dominio.com/fullchain.pem:/etc/nginx/ssl/fullchain.pem:ro \
  -v /etc/letsencrypt/live/seu-dominio.com/privkey.pem:/etc/nginx/ssl/privkey.pem:ro \
  --restart unless-stopped \
  ai_geologia_nginx
```

### 7. Verificar logs em produção
```bash
# Ver logs da aplicação
docker logs ai_geologia

# Ver logs do Nginx
docker logs ai_geologia_nginx
```

### 8. Manutenção em produção
```bash
# Atualizar a aplicação
docker pull ai_geologia:latest
docker stop ai_geologia
docker rm ai_geologia
# Rodar novamente o comando do passo 6

# Renovar certificados SSL (a cada 90 dias)
sudo certbot renew
docker restart ai_geologia_nginx
```

### 9. Backup
```bash
# Backup dos relatórios
tar -czf backup_relatorios_$(date +%Y%m%d).tar.gz /path/to/relatorios

# Backup dos certificados SSL
tar -czf backup_ssl_$(date +%Y%m%d).tar.gz /etc/letsencrypt
```

## Notas Importantes

1. Em desenvolvimento:
   - Usa HTTP na porta 80
   - Não requer SSL
   - Logs mais detalhados
   - Volume montado no diretório local

2. Em produção:
   - Usa HTTPS na porta 443
   - Requer certificados SSL
   - Redirecionamento automático de HTTP para HTTPS
   - Restart automático dos containers
   - Volume montado em diretório absoluto
   - Backup regular dos dados

3. Segurança:
   - Nunca commite certificados SSL
   - Mantenha backups regulares
   - Monitore os logs
   - Mantenha os certificados SSL atualizados