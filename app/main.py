import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import streamlit as st

# Asegurar que el directorio raíz esté en el PYTHONPATH
project_dir = Path(__file__).parent.parent.absolute()
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# Importaciones del proyecto
from app.config.configuration import Configuration
from app.utils.logger import Logger


class ACMADashboard:
    def __init__(self):
        # Importaciones locales dentro del __init__
        from app.components.auth import Auth
        from app.components.certificados import Certificados
        from app.components.chat import Chat
        from app.components.metrics_dashboard import MetricsDashboard
        from app.components.notifications import Notifications
        from app.components.report_generator import ReportGenerator
        from app.components.sidebar import Sidebar
        from app.components.solicitudes import Solicitudes

        self.config = Configuration()
        self.auth = Auth()
        self.sidebar = Sidebar()
        self.certificados = Certificados()
        self.solicitudes = Solicitudes()
        self.chat = Chat()
        self.notifications = Notifications()
        self.metrics_dashboard = MetricsDashboard()
        self.report_generator = ReportGenerator()
        self.setup_session_state()

    def setup_session_state(self) -> None:
        """Inicializa el estado de la sesión"""
        default_states = {
            'authenticated': False,
            'current_page': "home",
            'metrics_period': 30,
            'date_range': (datetime.now() - timedelta(days=30), datetime.now())
        }

        for key, value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def render(self) -> None:
        """Renderiza el dashboard"""
        try:
            self.sidebar.render()

            if not st.session_state.authenticated:
                st.warning("Por favor inicia sesión para acceder al dashboard")
                return

            # Redirigir 'main' a 'home'
            if st.session_state.get('current_page') == 'main':
                st.session_state.current_page = 'home'
                st.rerun()

            current_page = st.session_state.get('current_page', 'home')

            if current_page == "home":
                self.render_home()
            elif current_page == "certificates":
                self.render_certificates()
            elif current_page == "requests":
                self.render_requests()
            elif current_page == "settings":
                self.render_settings()
            else:
                st.error("Página no encontrada")

        except Exception as e:
            Logger.error(f"Error en dashboard: {str(e)}")
            st.error("Error cargando el dashboard")

    def render_home(self) -> None:
        """Renderiza la página de inicio"""
        try:
            from app.pages.home import render_home_page
            render_home_page()
        except Exception as e:
            Logger.error(f"Error en página de inicio: {str(e)}")
            st.error("Error cargando la página de inicio")

    def render_certificates(self) -> None:
        """Renderiza la página de certificados"""
        try:
            from app.pages.certificates import render_certificates_page
            render_certificates_page()
        except Exception as e:
            Logger.error(f"Error en página de certificados: {str(e)}")
            st.error("Error cargando la página de certificados")

    def render_requests(self) -> None:
        """Renderiza la página de solicitudes"""
        from app.pages.requests import render_requests_page
        render_requests_page()

    def render_settings(self) -> None:
        """Renderiza la página de configuración"""
        from app.pages.settings import SettingsPage
        settings_page = SettingsPage()
        settings_page.render()


def main():
    """Función principal de la aplicación"""
    try:
        # Cambiar al directorio del proyecto
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        dashboard = ACMADashboard()
        dashboard.render()
    except Exception as e:
        Logger.error(f"Error en main: {str(e)}")
        st.error("Error iniciando la aplicación")


if __name__ == "__main__":
    main()
