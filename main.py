from datetime import datetime
import os
import pytz
import warnings
from fastapi import FastAPI, Request
from message_whatsapp import MessageWhatsapp
from crew.geo_crew import GeoCrew
from send_whatsapp import SendWhatsapp
from transcribe_audio import transcribe_audio

# Suprimir warnings específicos do Pydantic
warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

app = FastAPI(title="Geology Report Generation API")

# Diretório para salvar os relatórios
relatorios_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relatorios")
os.makedirs(relatorios_dir, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Geology Report Generation API is running"}

async def process_and_send_report(text: str, wa_message: MessageWhatsapp) -> dict:
    """
    Processa o texto e envia o relatório via WhatsApp
    """
    # Gerar nome do arquivo baseado na data/hora
    tz = pytz.timezone('America/Sao_Paulo')
    file_name = datetime.now(tz).strftime("%Y-%m-%d_%H-%M-%S")
    
    # Executar o GeoCrew para gerar o relatório
    try:
        result = GeoCrew().run(text, file_name)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # Verificar se o PDF foi gerado
    pdf_path = os.path.join(relatorios_dir, f'relatorio_{file_name}.pdf')
    
    if os.path.exists(pdf_path):
        try:
            whatsapp = SendWhatsapp()
            response = whatsapp.send_pdf(
                number=wa_message.remote_jid.split('@')[0],
                pdf_file=pdf_path,
                caption="Aqui está seu relatório geológico!"
            )
            return {"status": "success", "message": "Relatório gerado e enviado com sucesso"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    return {"status": "error", "message": "Falha ao gerar o relatório"}

async def process_audio(audio_base64: str, wa_message: MessageWhatsapp) -> str:
    try:
        # Transcrever o áudio para texto
        text = transcribe_audio(audio_base64)
        # Enviar confirmação da transcrição
        whatsapp = SendWhatsapp()
        whatsapp.textMessage(
            number=wa_message.remote_jid.split('@')[0],
            msg=f"Áudio recebido! Transcrição: {text}\n\nGerando relatório..."
        )
        return text
    except Exception as e:
        return None

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Receber e processar os dados do webhook
        data = await request.json()
        
        # Criar instância de MessageWhatsapp
        wa_message = MessageWhatsapp(data)

        text = None
        
        # Verificar se há áudio
        if wa_message.message_type == wa_message.TYPE_AUDIO:
            audio_base64 = wa_message.get_audio()
            if audio_base64:
                text = await process_audio(audio_base64, wa_message)
                
        # Verificar se tem texto
        elif wa_message.message_type == wa_message.TYPE_TEXT:
            text = wa_message.get_text()
        
        # Se temos texto (seja da mensagem ou do áudio), processar
        if text:
            return "Texto recebido: " + text
            # return await process_and_send_report(text, wa_message)
        
        return {"status": "error", "message": "Nenhum texto ou áudio encontrado na mensagem"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6248)
