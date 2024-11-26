from services.ai_service_interface import AIServiceInterface
from config.secrets_manager import SecretsManager

class VertexService(AIServiceInterface):
    def __init__(self):
        self.project_id = SecretsManager.get_secret("GCP_PROJECT_ID")
        self.location = SecretsManager.get_secret("GCP_LOCATION")
        self._init_client()
        
    def _init_client(self):
        """
        Inicializa el cliente de Vertex AI.
        Por ahora es un placeholder.
        """
        pass
        
    def process_request(self, request_data):
        """
        Procesa una solicitud usando Vertex AI.
        """
        return {
            "response": f"Vertex AI procesó: {request_data}",
            "provider": "vertex"
        }
