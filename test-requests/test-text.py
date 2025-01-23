import requests
import json

# Defina o arquivo JSON
def load_test_data():
    with open('example-request/text-request2.json', 'r') as file:
        data = json.load(file)
        return data

data = load_test_data()

# Converta o dicionário para JSON
json_data = json.dumps(data)

# Defina o cabeçalho para informar que está enviando JSON
headers = {
    "Content-Type": "application/json"
}

# Faça a requisição POST
try:
    response = requests.post("http://localhost:6248/webhook", data=json_data, headers=headers)
    
    # Verifique o status da resposta
    if response.status_code == 200:
        print("Requisição bem-sucedida:", response.json())
    else:
        print("Erro na requisição:", response.status_code, response.text)
except requests.exceptions.RequestException as e:
    print("Erro ao fazer a requisição:", e)