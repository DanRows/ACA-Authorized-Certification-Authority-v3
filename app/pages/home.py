from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.components.certificados import Certificados
from app.components.dashboard_widgets import DashboardWidgets
from app.components.metrics_dashboard import MetricsDashboard
from app.components.solicitudes import Solicitudes
from app.utils.cache import CacheManager
from app.utils.logger import Logger


class HomePage:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            try:
                self.solicitudes = Solicitudes()
                self.certificados = Certificados()
                self.metrics = MetricsDashboard()
                self.widgets = DashboardWidgets(self.solicitudes, self.certificados)
                self.cache_manager = CacheManager()
                self._initialize_state()
                self.__class__._initialized = True
            except Exception as e:
                Logger.error(f"Error inicializando HomePage: {str(e)}")
                raise

    def _initialize_state(self) -> None:
        """Inicializa el estado de la página"""
        try:
            if 'home_view' not in st.session_state:
                st.session_state.home_view = "General"
            if 'date_range' not in st.session_state:
                st.session_state.date_range = [
                    datetime.now() - timedelta(days=30),
                    datetime.now()
                ]
            # Asegurarse de que haya datos de ejemplo
            self._add_sample_data()
        except Exception as e:
            Logger.error(f"Error inicializando estado: {str(e)}")
            raise

    def _add_sample_data(self) -> None:
        """Agrega datos de ejemplo si no hay datos"""
        try:
            if len(self.solicitudes.get_requests()) == 0:
                self.solicitudes.add_request({
                    'id': '001',
                    'status': 'pending',
                    'provider': 'openai',
                    'created_at': datetime.now()
                })
                self.solicitudes.add_request({
                    'id': '002',
                    'status': 'completed',
                    'provider': 'vertex',
                    'created_at': datetime.now()
                })

            if len(self.certificados.get_certificates()) == 0:
                self.certificados.add_certificate({
                    'id': '001',
                    'status': 'active',
                    'created_at': datetime.now(),
                    'details': {'type': 'basic'}
                })
                self.certificados.add_certificate({
                    'id': '002',
                    'status': 'pending',
                    'created_at': datetime.now(),
                    'details': {'type': 'advanced'}
                })
        except Exception as e:
            Logger.warning(f"No se pudieron agregar datos de ejemplo: {str(e)}")

    def render(self) -> None:
        """Renderiza la página de inicio"""
        try:
            st.title("Panel Principal ACMA")

            # Selector de vista y rango de fechas
            col1, col2 = st.columns([1, 2])
            with col1:
                st.session_state.home_view = st.radio(
                    "Vista",
                    options=["General", "Detallada"],
                    horizontal=True,
                    key="home_view_radio"
                )
            with col2:
                st.session_state.date_range = st.date_input(
                    "Rango de fechas",
                    value=st.session_state.date_range,
                    key="home_date_range"
                )

            # Renderizar vista seleccionada
            if st.session_state.home_view == "General":
                self._render_general_view()
            else:
                self._render_detailed_view()

        except Exception as e:
            Logger.error(f"Error en página de inicio: {str(e)}")
            st.error("Error cargando el panel principal")

    def _render_general_view(self) -> None:
        """Renderiza vista general"""
        try:
            # Asegurarse de que haya datos
            if len(self.solicitudes.get_requests()) == 0:
                self._add_sample_data()

            # Métricas principales
            self.widgets.show_metrics_card()

            # Línea de tiempo
            self.widgets.show_requests_timeline()

            # Estadísticas por proveedor
            self.widgets.show_provider_stats()

        except Exception as e:
            Logger.error(f"Error en vista general: {str(e)}")
            st.error("Error cargando vista general")

    def _render_detailed_view(self) -> None:
        """Renderiza vista detallada"""
        try:
            # Panel de métricas completo
            self.metrics.render()
        except Exception as e:
            Logger.error(f"Error en vista detallada: {str(e)}")
            st.error("Error cargando vista detallada")


def render_home_page():
    """Punto de entrada para la página de inicio"""
    try:
        page = HomePage()
        page.render()
    except Exception as e:
        Logger.error(f"Error en render_home_page: {str(e)}")
        st.error("Error cargando la página de inicio")
