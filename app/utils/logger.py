import logging
from typing import Any


class Logger:
    _logger = None

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            cls._logger = logging.getLogger('acma_dashboard')
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            cls._logger.addHandler(handler)
            cls._logger.setLevel(logging.INFO)
        return cls._logger

    @classmethod
    def info(cls, message: Any) -> None:
        cls._get_logger().info(message)

    @classmethod
    def error(cls, message: Any) -> None:
        cls._get_logger().error(message)

    @classmethod
    def warning(cls, message: Any) -> None:
        cls._get_logger().warning(message)

    @classmethod
    def debug(cls, message: Any) -> None:
        cls._get_logger().debug(message)
