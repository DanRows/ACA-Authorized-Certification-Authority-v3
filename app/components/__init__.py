"""
Componentes del ACMA Dashboard
-----------------------------
Este paquete contiene los componentes principales de la aplicación.
"""

from .auth import Auth
from .certificados import Certificados
from .chat import Chat
from .dashboard_widgets import DashboardWidgets
from .metrics_dashboard import MetricsDashboard
from .notifications import Notifications
from .report_generator import ReportGenerator
from .sidebar import Sidebar
from .solicitudes import Solicitudes

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
