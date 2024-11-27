"""
ACMA Dashboard
-------------
Un dashboard modular y escalable para gestión de certificados y solicitudes.
"""

from .config.configuration import Configuration
from .config.secrets_manager import SecretsManager
from .services.ai_service_interface import AIServiceInterface
from .services.factory import ServiceFactory
from .utils.cache import CacheManager, cached
from .utils.logger import Logger

__version__ = "0.1.0"

__all__ = [
    'Configuration',
    'SecretsManager',
    'AIServiceInterface',
    'ServiceFactory',
    'Logger',
    'CacheManager',
    'cached'
]
