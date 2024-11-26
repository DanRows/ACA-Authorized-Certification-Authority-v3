from typing import Dict, Type
from services.ai_service_interface import AIServiceInterface
from services.openai_service import OpenAIService
from services.vertex_service import VertexService
from services.sambanova_service import SambaNovaService

class ServiceFactory:
    _services: Dict[str, Type[AIServiceInterface]] = {
        "openai": OpenAIService,
        "vertex": VertexService,
        "sambanova": SambaNovaService
    }
    
    @classmethod
    def register_service(cls, name: str, service_class: Type[AIServiceInterface]):
        """
        Registra un nuevo servicio de IA.
        """
        cls._services[name] = service_class
    
    @classmethod
    def create_service(cls, provider: str) -> AIServiceInterface:
        """
        Crea una instancia del servicio de IA especificado.
        """
        if provider not in cls._services:
            raise ValueError(f"Proveedor no soportado: {provider}")
            
        service_class = cls._services[provider]
        return service_class()
        
    @classmethod
    def get_available_providers(cls) -> list:
        """
        Retorna la lista de proveedores disponibles.
        """
        return list(cls._services.keys())