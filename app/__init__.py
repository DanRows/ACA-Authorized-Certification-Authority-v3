"""
ACMA Dashboard
-------------
Un dashboard modular y escalable para gestión de certificados y solicitudes.
"""

import os
import sys
from pathlib import Path

# Asegurar que el directorio raíz esté en el PYTHONPATH
project_dir = Path(__file__).parent.parent.absolute()
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# Importaciones del proyecto
from app.config.configuration import Configuration
from app.config.secrets_manager import SecretsManager
from app.services.ai_service_interface import AIServiceInterface
from app.services.factory import ServiceFactory
from app.utils.cache import CacheManager, cached
from app.utils.logger import Logger

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
