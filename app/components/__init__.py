"""
Componentes del ACMA Dashboard
-----------------------------
Este paquete contiene los componentes principales de la aplicación.
"""

# Importaciones básicas primero
from app.components.auth import Auth
from app.components.certificados import Certificados
from app.components.chat import Chat
from app.components.dashboard_widgets import DashboardWidgets

# Importaciones que dependen de las básicas
from app.components.metrics_dashboard import MetricsDashboard
from app.components.notifications import Notifications
from app.components.report_generator import ReportGenerator
from app.components.sidebar import Sidebar
from app.components.solicitudes import Solicitudes

__all__ = [
    'Auth',
    'Certificados',
    'Solicitudes',
    'Notifications',
    'MetricsDashboard',
    'DashboardWidgets',
    'Sidebar',
    'Chat',
    'ReportGenerator'
]
