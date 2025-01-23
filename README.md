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
      "conversation": "Gerar relatório para terreno.."
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
