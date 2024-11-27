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

            # Análisis detallado
            st.header("Análisis Detallado")
            self._render_detailed_analysis()

        except Exception as e:
            Logger.error(f"Error en dashboard de métricas: {str(e)}")
            st.error("Error cargando métricas")

    def _render_detailed_analysis(self) -> None:
        """Renderiza análisis detallado"""
        try:
            col1, col2 = st.columns(2)

            with col1:
                self._render_provider_distribution()
            with col2:
                self._render_status_distribution()

        except Exception as e:
            Logger.error(f"Error en análisis detallado: {str(e)}")
            st.error("Error mostrando análisis detallado")

    def _render_provider_distribution(self) -> None:
        """Renderiza distribución por proveedor"""
        try:
            providers = self.solicitudes.get_provider_stats()
            fig = px.pie(
                values=list(providers.values()),
                names=list(providers.keys()),
                title="Distribución por Proveedor"
            )
            st.plotly_chart(fig)
        except Exception as e:
            Logger.error(f"Error en distribución de proveedores: {str(e)}")
            st.error("Error mostrando distribución de proveedores")

    def _render_status_distribution(self) -> None:
        """Renderiza distribución por estado"""
        try:
            requests = self.solicitudes.get_requests()
            status_counts = {}
            for request in requests:
                status = request.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1

            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Distribución por Estado"
            )
            st.plotly_chart(fig)
        except Exception as e:
            Logger.error(f"Error en distribución de estados: {str(e)}")
            st.error("Error mostrando distribución de estados")

    def get_metrics_summary(self) -> Dict:
        """Obtiene resumen de métricas"""
        try:
            requests = self.solicitudes.get_requests()
            certificates = self.certificados.get_certificates()

            return {
                'total_requests': len(requests),
                'pending_requests': len([r for r in requests if r['status'] == 'pending']),
                'total_certificates': len(certificates),
                'success_rate': self._calculate_success_rate(requests)
            }
        except Exception as e:
            Logger.error(f"Error obteniendo métricas: {str(e)}")
            return {}

    def _calculate_success_rate(self, requests: List[Dict]) -> float:
        """Calcula la tasa de éxito de las solicitudes"""
        try:
            if not requests:
                return 100.0
            completed = len([r for r in requests if r['status'] == 'completed'])
            return round((completed / len(requests)) * 100, 2)
        except Exception as e:
            Logger.error(f"Error calculando tasa de éxito: {str(e)}")
            return 0.0
