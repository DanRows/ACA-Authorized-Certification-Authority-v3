from typing import List

from app.utils.logger import Logger


class ServiceFactory:
    _providers = ['openai', 'vertex', 'sambanova']

    @classmethod
    def get_available_providers(cls) -> List[str]:
        return cls._providers

    @classmethod
    def create_service(cls, provider: str):
        try:
            if provider not in cls._providers:
                raise ValueError(f"Proveedor no soportado: {provider}")

            # Aquí iría la lógica de creación del servicio
            return None

        except Exception as e:
            Logger.error(f"Error creando servicio: {str(e)}")
            raise
