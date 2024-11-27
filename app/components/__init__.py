"""
Componentes del ACMA Dashboard
-----------------------------
Este paquete contiene los componentes principales de la aplicación.
"""

from app.components.auth import Auth
from app.components.certificados import Certificados
from app.components.chat import Chat
from app.components.dashboard_widgets import DashboardWidgets
from app.components.metrics_dashboard import MetricsDashboard
from app.components.notifications import Notifications
from app.components.report_generator import ReportGenerator
from app.components.sidebar import Sidebar
from app.components.solicitudes import Solicitudes

__all__ = [
    'Auth',
    'Certificados',
    'Chat',
    'DashboardWidgets',
    'MetricsDashboard',
    'Notifications',
    'ReportGenerator',
    'Sidebar',
    'Solicitudes'
]
