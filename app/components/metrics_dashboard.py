from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.dashboard_widgets import DashboardWidgets
from services.metrics_service import MetricsService
from utils.logger import Logger


class MetricsDashboard:
    def __init__(self):
        self.metrics_service = MetricsService()
        self.widgets = DashboardWidgets(
            self.metrics_service.solicitudes,
            self.metrics_service.certificados
        )

    def render(self) -> None:
        try:
            st.title("Panel de Métricas")
            days = st.slider(
                "Período de análisis (días)",
                min_value=7,
                max_value=90,
                value=st.session_state.metrics_period
            )

            metrics = self.metrics_service.get_dashboard_metrics(days)
            self.widgets.show_metrics_card()
            self._render_charts(metrics)

        except Exception as e:
            Logger.error(f"Error en dashboard de métricas: {str(e)}")
            st.error("Error cargando métricas")

    def _render_charts(self, metrics: Dict) -> None:
        st.subheader("Gráficos de Rendimiento")
        col1, col2 = st.columns(2)

        with col1:
            self.widgets.show_requests_timeline()
        with col2:
            self.widgets.show_provider_stats()
