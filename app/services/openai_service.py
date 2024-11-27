from typing import Dict

from app.config.secrets_manager import SecretsManager
from app.services.ai_service_interface import AIServiceInterface
from app.utils.logger import Logger


class OpenAIService(AIServiceInterface):
    def __init__(self):
        self.api_key = SecretsManager.get_secret("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"  # modelo por defecto

    def get_completion(self, prompt: str) -> str:
        """
        Obtiene una respuesta del modelo OpenAI.

        Args:
            prompt: El texto de entrada para el modelo

        Returns:
            La respuesta generada por el modelo
        """
        try:
            # Aquí iría la llamada real a la API de OpenAI
            return f"OpenAI respuesta simulada para: {prompt}"
        except Exception as e:
            Logger.error(f"Error en OpenAI completion: {str(e)}")
            raise

    def process_request(self, request_data: Dict) -> Dict:
        """
        Procesa una solicitud usando OpenAI.

        Args:
            request_data: Datos de la solicitud

        Returns:
            Respuesta procesada
        """
        try:
            return {
                "response": f"OpenAI procesó: {request_data}",
                "provider": "openai"
            }
        except Exception as e:
            Logger.error(f"Error procesando solicitud OpenAI: {str(e)}")
            raise
