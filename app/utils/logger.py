import logging
from datetime import datetime
from pathlib import Path
from typing import Any


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Inicializa el logger"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger("ACMA")
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Archivo de log
        file_handler = logging.FileHandler(
            f"logs/acma_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    @classmethod
    def info(cls, message: Any) -> None:
        """Registra un mensaje informativo"""
        cls()._log('info', message)

    @classmethod
    def error(cls, message: Any) -> None:
        """Registra un mensaje de error"""
        cls()._log('error', message)

    @classmethod
    def warning(cls, message: Any) -> None:
        """Registra un mensaje de advertencia"""
        cls()._log('warning', message)

    @classmethod
    def debug(cls, message: Any) -> None:
        """Registra un mensaje de depuración"""
        cls()._log('debug', message)

    def _log(self, level: str, message: Any) -> None:
        """Registra un mensaje en el nivel especificado"""
        getattr(self.logger, level)(message)
