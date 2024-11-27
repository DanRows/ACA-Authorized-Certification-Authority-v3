"""
ACMA Dashboard
-------------
Un dashboard modular y escalable para gestión de certificados y solicitudes.
"""

__version__ = "0.1.0"

# Evitar importaciones aquí para prevenir ciclos
__all__ = [
    'Configuration',
    'SecretsManager',
    'AIServiceInterface',
    'ServiceFactory',
    'Logger',
    'CacheManager',
    'cached'
]
