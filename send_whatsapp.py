import os
import base64
import requests
from dotenv import load_dotenv
from evolutionapi.client import EvolutionClient
from evolutionapi.models.message import TextMessage, MediaMessage

class SendWhatsapp:
    
    def __init__(self) -> None:
        # Carregar variáveis de ambiente
        load_dotenv()
        self.evo_api_token = os.getenv("EVOLUTION_API_TOKEN")
        self.evo_instance_id = os.getenv("EVOLUTION_INSTANCE")
        self.evo_instance_token = os.getenv("EVOLUTION_INSTANCE_TOKEN")
        self.evo_base_url = os.getenv("EVOLUTION_BASE_URL")
        
        # Inicializar o cliente Evolution
        self.client = EvolutionClient(
            base_url=self.evo_base_url,
            api_token=self.evo_api_token
        )

    def textMessage(self, number, msg, mentions=[]):
        # Enviar mensagem de texto
        text_message = TextMessage(
            number=str(number),
            text=msg,
            mentioned=mentions
        )

        response = self.client.messages.send_text(
            self.evo_instance_id, 
            text_message, 
            self.evo_instance_token
        )
        return response

    def send_pdf(self, number, pdf_file, caption=""):
        # Enviar PDF
        url = f"{self.evo_base_url}/message/sendMedia/{self.evo_instance_id}"
        
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(pdf_file):
                raise FileNotFoundError(f"Arquivo não encontrado: {pdf_file}")
            
            # Ler o arquivo PDF
            with open(pdf_file, 'rb') as file:
                pdf_content = file.read()
            
            # Codificar o conteúdo em base64
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            headers = {
                "Content-Type": "application/json",
                "apikey": self.evo_api_token
            }
            
            data = {
                "number": number,
                "mediatype": "document",
                "media": pdf_base64,
                "fileName": os.path.basename(pdf_file),
                "mimetype": "application/pdf"
            }
            
            if caption:
                data["caption"] = caption
            
            response = requests.post(url, headers=headers, json=data)
            return response.json()
            
        except Exception as e:
            raise

    def audio(self, number, audio_file):
        # Enviar áudio
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Arquivo '{audio_file}' não encontrado.")

        audio_message = {
            "number": number,
            "mediatype": "audio",
            "mimetype": "audio/mpeg",
            "caption": ""
        }
            
        self.client.messages.send_whatsapp_audio(
            self.evo_instance_id,
            audio_message,
            self.evo_instance_token,
            audio_file
        )
                    
        return "Áudio enviado"

    def image(self, number, image_file, caption=""):
        # Enviar imagem
        if not os.path.exists(image_file):
            raise FileNotFoundError(f"Arquivo '{image_file}' não encontrado.")

        media_message = MediaMessage(
            number=number,
            mediatype="image",
            mimetype="image/jpeg",
            caption=caption,
            fileName=os.path.basename(image_file),
            media=""
        )

        self.client.messages.send_media(
            self.evo_instance_id, 
            media_message, 
            self.evo_instance_token,
            image_file
        )
        
        return "Imagem enviada"

    def video(self, number, video_file, caption=""):
        # Enviar vídeo
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Arquivo '{video_file}' não encontrado.")

        media_message = MediaMessage(
            number=number,
            mediatype="video",
            mimetype="video/mp4",
            caption=caption,
            fileName=os.path.basename(video_file),
            media=""
        )

        self.client.messages.send_media(
            self.evo_instance_id, 
            media_message, 
            self.evo_instance_token,
            video_file
        )
        
        return "Vídeo enviado"

    def document(self, number, document_file, caption=""):
        # Enviar documento
        if not os.path.exists(document_file):
            raise FileNotFoundError(f"Arquivo '{document_file}' não encontrado.")

        media_message = MediaMessage(
            number=number,
            mediatype="document",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            caption=caption,
            fileName=os.path.basename(document_file),
            media=""
        )

        self.client.messages.send_media(
            self.evo_instance_id, 
            media_message, 
            self.evo_instance_token,
            document_file
        )
        
        return "Documento enviado"
