import json
import requests
import warnings
from typing import Dict, Any

# Suprimir warnings específicos do Pydantic
warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

def test_webhook():
    # Carregar o exemplo de request com áudio
    with open("example-request/audio-request.json", "r") as f:
        request_data: Dict[str, Any] = json.load(f)
    
    # URL do webhook (usando o nome do serviço do Docker)
    webhook_url = "http://geologia_app:6248/webhook"
    
    try:
        # Enviar o request para o webhook
        response = requests.post(webhook_url, json=request_data)
        
        # Verificar se a requisição foi bem sucedida
        response.raise_for_status()
        
        print("Request enviado com sucesso!")
        print("Status code:", response.status_code)
        print("Resposta:", response.json())
        
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar request:", str(e))
    except json.JSONDecodeError:
        print("Erro ao decodificar resposta JSON")
        print("Resposta texto:", response.text)

if __name__ == "__main__":
    test_webhook()
