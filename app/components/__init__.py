"""
Componentes del ACMA Dashboard
-----------------------------
Este paquete contiene los componentes principales de la aplicación.
"""

# Importaciones básicas
from app.components.auth import Auth
from app.components.certificados import Certificados

# Importaciones de funcionalidad
from app.components.chat import Chat

# Importaciones de UI
from app.components.notifications import Notifications
from app.components.report_generator import ReportGenerator
from app.components.sidebar import Sidebar
from app.components.solicitudes import Solicitudes

__all__ = [
    'Auth',
    'Certificados',
    'Solicitudes',
    'Notifications',
    'Sidebar',
    'Chat',
    'ReportGenerator'
]
