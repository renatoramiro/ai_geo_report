import os
import base64
import tempfile
from litellm import transcription
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(
    base64_audio: str,
    language: str = 'pt',
    prompt: str = "",
    model: str = 'groq/whisper-large-v3'
) -> str:
    """
    Transcribe audio from base64 string to text

    Args:
        base64_audio: Base64 encoded audio string
        language: Language code (default: 'pt')
        prompt: Optional prompt to guide transcription
        model: Model to use for transcription

    Returns:
        str: Transcribed text
    """
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            decoded_audio = base64.b64decode(base64_audio)
            temp_audio.write(decoded_audio)
            temp_audio_path = temp_audio.name

        with open(temp_audio_path, "rb") as audio_file:
            transcript = transcription(
                model=model,
                file=audio_file,
                prompt=prompt,
                temperature=0.0,
                language=language,
                response_format="json"
            )
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
    
    return str(transcript.text)