from typing import Any, Dict, Optional

from app.utils.logger import Logger


class Configuration:
    def __init__(self):
        self.settings: Dict[str, Any] = {
            "database": {
                "postgresql": "postgresql://user:password@localhost/acma_db",
                "sqlite": "sqlite:///acma.db",
                "active": "sqlite"  # o "postgresql"
            },
            "ai_providers": {
                "openai": {
                    "api_key": "",
                    "available_models": ["gpt-3.5-turbo", "gpt-4"],
                    "max_tokens": 2048
                },
                "vertex": {
                    "project_id": "",
                    "location": "us-central1",
                    "available_models": ["text-bison", "chat-bison"],
                    "max_tokens": 1024
                },
                "sambanova": {
                    "api_key": "",
                    "endpoint": "",
                    "available_models": ["basic", "advanced"],
                    "max_tokens": 2048
                }
            },
            "default_provider": "openai",
            "request_timeout": 30,
            "max_retries": 3,
            "retry_delay": 1,
            "performance": {
                "cache_ttl": 300,
                "max_threads": 4
            },
            "notifications": {
                "enable_email": False,
                "email_frequency": "Diaria"
            }
        }

    def get_setting(self, key: str) -> Optional[Any]:
        """
        Obtiene una configuración por su clave.

        Args:
            key: La clave de la configuración

        Returns:
            El valor de la configuración o None si no existe
        """
        try:
            return self.settings.get(key)
        except Exception as e:
            Logger.error(f"Error obteniendo configuración {key}: {str(e)}")
            return None

    def update_setting(self, key: str, value: Any) -> bool:
        """
        Actualiza una configuración.

        Args:
            key: La clave de la configuración
            value: El nuevo valor

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            self.settings[key] = value
            Logger.info(f"Configuración {key} actualizada")
            return True
        except Exception as e:
            Logger.error(f"Error actualizando configuración {key}: {str(e)}")
            return False

    def delete_setting(self, key: str) -> bool:
        """
        Elimina una configuración.

        Args:
            key: La clave de la configuración a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            if key in self.settings:
                del self.settings[key]
                Logger.info(f"Configuración {key} eliminada")
                return True
            return False
        except Exception as e:
            Logger.error(f"Error eliminando configuración {key}: {str(e)}")
            return False
