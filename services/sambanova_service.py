from services.ai_service_interface import AIServiceInterface
from config.secrets_manager import SecretsManager

class SambaNovaService(AIServiceInterface):
    def __init__(self):
        self.api_key = SecretsManager.get_secret("SAMBANOVA_API_KEY")
        self.endpoint = SecretsManager.get_secret("SAMBANOVA_ENDPOINT")
        
    def process_request(self, request_data):
        """
        Procesa una solicitud usando SambaNova.
        """
        return {
            "response": f"SambaNova procesó: {request_data}",
            "provider": "sambanova"
        } 
