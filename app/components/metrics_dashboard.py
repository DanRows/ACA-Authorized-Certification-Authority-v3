from datetime import datetime, timedelta
from typing import Dict, List

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.components.certificados import Certificados
from app.components.dashboard_widgets import DashboardWidgets
from app.components.solicitudes import Solicitudes
from app.utils.logger import Logger


class MetricsDashboard:
    def __init__(self):
        self.solicitudes = Solicitudes()
        self.certificados = Certificados()
        self.widgets = DashboardWidgets(self.solicitudes, self.certificados)

    def render(self) -> None:
        """Renderiza el dashboard de métricas"""
        try:
            # Métricas principales
            self.widgets.show_metrics_card()

            # Gráficos
            col1, col2 = st.columns(2)
            with col1:
                self.widgets.show_requests_timeline()
            with col2:
                self.widgets.show_provider_stats()

        except Exception as e:
            Logger.error(f"Error en dashboard de métricas: {str(e)}")
            st.error("Error cargando métricas")
