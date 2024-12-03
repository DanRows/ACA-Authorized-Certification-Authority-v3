"""
Componentes del ACMA Dashboard
-----------------------------
Este paquete contiene los componentes principales de la aplicación.
"""

# Importaciones básicas
from app.components.auth import Auth
from app.components.certificados import Certificados
from app.components.sidebar import Sidebar
from app.components.solicitudes import Solicitudes

__all__ = [
    'Auth',
    'Certificados',
    'Solicitudes',
    'Sidebar'
]
