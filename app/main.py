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
        # Importaciones básicas primero
        from app.components.auth import Auth
        from app.components.certificados import Certificados
        from app.components.sidebar import Sidebar
        from app.components.solicitudes import Solicitudes

        # Inicializar componentes básicos
        self.config = Configuration()
        self.auth = Auth()
        self.certificados = Certificados()
        self.solicitudes = Solicitudes()
        self.sidebar = Sidebar()

        # Ahora importar e inicializar componentes que dependen de los básicos
        from app.components.dashboard_widgets import DashboardWidgets
        from app.components.metrics_dashboard import MetricsDashboard

        self.dashboard = DashboardWidgets(self.solicitudes, self.certificados)
        self.metrics = MetricsDashboard()

        # Inicializar estado
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

            current_page = st.session_state.get('current_page', 'home')

            # Renderizar la página correspondiente
            if current_page == "home":
                self.metrics.render()
            elif current_page == "certificates":
                self.certificados_page()
            elif current_page == "requests":
                self.requests_page()
            elif current_page == "settings":
                self.settings_page()
            else:
                st.error("Página no encontrada")

        except Exception as e:
            Logger.error(f"Error en dashboard: {str(e)}")
            st.error("Error cargando el dashboard")

    def certificados_page(self) -> None:
        """Renderiza la página de certificados"""
        try:
            st.title("Gestión de Certificados")
            certificates = self.certificados.get_certificates()

            if not certificates:
                st.info("No hay certificados disponibles")
                return

            for cert in certificates:
                with st.expander(f"Certificado {cert['id']}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Fecha: {cert['created_at']}")
                        st.write(f"Estado: {cert.get('status', 'N/A')}")
                    with col2:
                        if cert.get('details'):
                            st.json(cert['details'])

        except Exception as e:
            Logger.error(f"Error en página de certificados: {str(e)}")
            st.error("Error cargando certificados")

    def requests_page(self) -> None:
        """Renderiza la página de solicitudes"""
        from app.pages.requests import render_requests_page
        render_requests_page()

    def settings_page(self) -> None:
        """Renderiza la página de configuración"""
        from app.pages.settings import SettingsPage
        settings_page = SettingsPage()
        settings_page.render()


def main():
    """Función principal de la aplicación"""
    try:
        # Cambiar al directorio del proyecto
        os.chdir(project_dir)

        dashboard = ACMADashboard()
        dashboard.render()
    except Exception as e:
        Logger.error(f"Error en main: {str(e)}")
        st.error("Error iniciando la aplicación")


if __name__ == "__main__":
    main()
