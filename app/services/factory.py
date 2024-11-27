from typing import Dict, List, Type

from app.services.ai_service_interface import AIServiceInterface
from app.services.openai_service import OpenAIService
from app.services.sambanova_service import SambaNovaService
from app.services.vertex_service import VertexService
from app.utils.logger import Logger


class ServiceFactory:
    _services: Dict[str, Type[AIServiceInterface]] = {
        "openai": OpenAIService,
        "vertex": VertexService,
        "sambanova": SambaNovaService
    }

    @classmethod
    def get_service(cls, provider: str) -> AIServiceInterface:
        """
        Obtiene una instancia del servicio de IA especificado.

        Args:
            provider: El nombre del proveedor de IA

        Returns:
            Una instancia del servicio de IA
        """
        try:
            if provider not in cls._services:
                raise ValueError(f"Proveedor no soportado: {provider}")

            service_class = cls._services[provider]
            return service_class()

        except Exception as e:
            Logger.error(f"Error creando servicio: {str(e)}")
            raise

    @classmethod
    def get_available_providers(cls) -> List[str]:
        """
        Retorna la lista de proveedores disponibles.

        Returns:
            Lista de nombres de proveedores
        """
        return list(cls._services.keys())

    @classmethod
    def register_service(cls, name: str, service_class: Type[AIServiceInterface]) -> None:
        """
        Registra un nuevo servicio de IA.

        Args:
            name: Nombre del servicio
            service_class: Clase que implementa AIServiceInterface
        """
        cls._services[name] = service_class
