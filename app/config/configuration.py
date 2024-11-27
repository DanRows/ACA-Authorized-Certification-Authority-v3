from typing import Any, Dict, Optional

from utils.logger import Logger


class Configuration:
    def __init__(self):
        self.settings = {
            "database_url": "postgresql://user:password@localhost/acma_db",
            "ai_providers": ["openai", "vertex", "sambanova"],
            "default_provider": "openai",
            "request_timeout": 30,
            "max_retries": 3,
            "retry_delay": 1
        }

    def get_setting(self, key: str) -> Any:
        try:
            return self.settings[key]
        except KeyError as e:
            Logger.error(f"Configuración no encontrada: {str(e)}")
            return None

    def update_setting(self, key: str, value: Any) -> None:
        try:
            self.settings[key] = value
            Logger.info(f"Configuración actualizada: {key}")
        except Exception as e:
            Logger.error(f"Error actualizando configuración: {str(e)}")
            raise
