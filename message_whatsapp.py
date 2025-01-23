class MessageWhatsapp:
    
    TYPE_TEXT = "conversation"  # Alterado para "conversation" para corresponder ao tipo real
    TYPE_IMAGE = "image"
    TYPE_VIDEO = "video"
    TYPE_AUDIO = "audioMessage"
    TYPE_DOCUMENT = "document"
    TYPE_LOCATION = "location"
    TYPE_CONTACT = "contact"
    TYPE_STICKER = "sticker"
    TYPE_TEMPLATE = "template"
    TYPE_BUTTON = "button"
    TYPE_LIST = "list"
    TYPE_ORDER = "order"
    TYPE_CALL = "call"
    TYPE_UNKNOWN = "unknown"

    SCOPE_GROUP = "group"
    SCOPE_PRIVATE = "private"
    
    def __init__(self, data):
        self.data = data
        self.remote_jid = None
        self.message_type = None
        self.text = None
        self.audio_base64 = None
        self.scope = self.SCOPE_PRIVATE  # Default para mensagens privadas
        self.extract_data()

    def extract_data(self):
        try:
            # Extrair remote_jid
            if 'data' in self.data and 'key' in self.data['data'] and 'remoteJid' in self.data['data']['key']:
                self.remote_jid = self.data['data']['key']['remoteJid']

            # Extrair tipo de mensagem e conteúdo
            if 'data' in self.data and 'message' in self.data['data']:
                message = self.data['data']['message']
                
                # Se tiver messageType no data, usar ele
                if 'messageType' in self.data['data']:
                    self.message_type = self.data['data']['messageType']
                # Se não, tentar determinar pelo conteúdo
                elif 'conversation' in message:
                    self.message_type = self.TYPE_TEXT
                elif 'audioMessage' in message:
                    self.message_type = self.TYPE_AUDIO
                else:
                    self.message_type = self.TYPE_UNKNOWN
                
                # Extrair o texto da mensagem
                if 'conversation' in message:
                    self.text = message['conversation']
                
                # Extrair áudio base64 se presente
                if 'audioMessage' in message and 'base64' in message:
                    self.audio_base64 = message['base64']
            else:
                self.message_type = self.TYPE_UNKNOWN

            # Determina o escopo da mensagem se tivermos um remote_jid
            if self.remote_jid:
                self.determine_scope()

        except Exception as e:
            raise

    def determine_scope(self):
        """Determina se a mensagem é de grupo ou privada e define os atributos correspondentes."""
        if self.remote_jid.endswith("@g.us"):
            self.scope = self.SCOPE_GROUP
            self.group_id = self.remote_jid.split("@")[0]  # ID do grupo
            self.phone = self.data['data']['key']['participant'].split("@")[0] if 'participant' in self.data['data']['key'] else None  # Número do remetente no grupo
        else:
            self.scope = self.SCOPE_PRIVATE
            self.phone = self.remote_jid.split("@")[0] if self.remote_jid else None  # Número do remetente

    def extract_specific_data(self):
        """Não precisamos mais deste método pois já extraímos tudo em extract_data"""
        pass

    def get_text(self):
        """Retorna o texto da mensagem ou string vazia se não houver texto"""
        return self.text if self.text else ""
    
    def get_audio(self):
        """Retorna o áudio base64 da mensagem ou None se não houver áudio"""
        return self.audio_base64
