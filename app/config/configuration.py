from typing import Any, Dict, Optional

from app.utils.logger import Logger


class Configuration:
    def __init__(self):
        self._settings = {
            "default_provider": "openai",
            "cache_ttl": 3600,
            "max_retries": 3
        }

    def get_setting(self, key: str) -> Any:
        try:
            return self._settings[key]
        except KeyError as e:
            Logger.error(f"Configuración no encontrada: {str(e)}")
            return None

    def update_setting(self, key: str, value: Any) -> None:
        try:
            self._settings[key] = value
            Logger.info(f"Configuración actualizada: {key}")
        except Exception as e:
            Logger.error(f"Error actualizando configuración: {str(e)}")
            raise
