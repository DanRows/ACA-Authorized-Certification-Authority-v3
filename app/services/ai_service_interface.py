from abc import ABC, abstractmethod
from typing import Optional


class AIServiceInterface(ABC):
    """Interfaz base para servicios de IA"""

    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        """
        Obtiene una respuesta del modelo de IA.

        Args:
            prompt: El texto de entrada para el modelo

        Returns:
            La respuesta generada por el modelo
        """
        pass

    @abstractmethod
    def process_request(self, request_data: dict) -> dict:
        """
        Procesa una solicitud y retorna una respuesta.

        Args:
            request_data: Datos de la solicitud

        Returns:
            Respuesta procesada
        """
        pass
