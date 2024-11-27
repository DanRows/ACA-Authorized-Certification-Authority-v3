"""
Componentes del ACMA Dashboard
-----------------------------
Este paquete contiene los componentes principales de la aplicación.
"""

import os
import sys
from pathlib import Path

# Asegurar que el directorio raíz esté en el PYTHONPATH
project_dir = Path(__file__).parent.parent.parent.absolute()
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# Importaciones del proyecto
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
