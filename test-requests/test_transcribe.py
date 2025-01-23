import json
import os
import sys
import warnings
from typing import Dict, Any

# Suprimir warnings específicos do Pydantic
warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transcribe_audio import transcribe_audio

def test_transcribe():
    # Carregar o exemplo de request com áudio
    with open("example-request/audio-request.json", "r") as f:
        request_data: Dict[str, Any] = json.load(f)
    
    # Extrair o áudio base64 da mensagem
    audio_base64 = request_data["data"]["message"].get("base64", "")
    if not audio_base64:
        print("Erro: Áudio base64 não encontrado na mensagem")
        return
    
    # Testar a transcrição
    try:
        transcription = transcribe_audio(audio_base64)
        print("Transcrição bem sucedida!")
        print("Texto transcrito:", transcription)
    except Exception as e:
        print("Erro na transcrição:", str(e))

if __name__ == "__main__":
    test_transcribe()
