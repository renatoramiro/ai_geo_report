from datetime import datetime
import os
import pytz
import warnings
import logging
from fastapi import FastAPI, Request
from message_whatsapp import MessageWhatsapp
from crew.geo_crew import GeoCrew
from writing_style_crew.writing_style_crew import WritingStyleCrew
from read_template_crew import ReadTemplateCrew

from send_whatsapp import SendWhatsapp
from transcribe_audio import transcribe_audio

# Configure logging to suppress debug messages
logging.basicConfig(level=logging.INFO)

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
    try:
        # Criar instância do SendWhatsapp
        whatsapp = SendWhatsapp()
        
        # Enviar mensagem de confirmação
        whatsapp.textMessage(
            number=wa_message.remote_jid.split('@')[0],
            msg="Recebido! Estou gerando seu relatório, por favor aguarde..."
        )
        
        # Gerar nome do arquivo baseado no timestamp
        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y%m%d_%H%M%S')
        file_name = f"relatorio_{timestamp}"

        read_template_crew = ReadTemplateCrew()
        template_path = 'meu_template.pdf'
        template_crew_result = read_template_crew.run(file_path=template_path)

        write_style_crew = WritingStyleCrew()
        response_write_style = write_style_crew.run()

        # Criar instância do GeoCrew
        crew = GeoCrew()
        
        # Executar o processo
        result = crew.run(text, file_name, response_write_style, template_crew_result)
        
        # Verificar se os arquivos foram gerados
        pdf_file = os.path.join(relatorios_dir, f'{file_name}.pdf')
        docx_file = os.path.join(relatorios_dir, f'{file_name}.docx')
        
        if not os.path.exists(pdf_file) or not os.path.exists(docx_file):
            return {"status": "error", "message": "Falha ao gerar os arquivos do relatório"}
        
        # Enviar o PDF
        whatsapp.send_pdf(
            number=wa_message.remote_jid.split('@')[0],
            pdf_file=pdf_file,
            caption="Aqui está seu relatório em PDF!"
        )
        
        # Enviar o DOCX
        whatsapp.send_document(
            number=wa_message.remote_jid.split('@')[0],
            document_file=docx_file,
            caption="E aqui está a versão editável em Word!"
        )
        
        return {"status": "success", "message": "Relatório gerado e enviado com sucesso!"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

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
            # return "Texto recebido: " + text
            return await process_and_send_report(text, wa_message)
        
        return {"status": "error", "message": "Nenhum texto ou áudio encontrado na mensagem"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6248)
