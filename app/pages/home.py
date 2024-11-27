from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

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
    def __init__(self):
        self.solicitudes = Solicitudes()
        self.certificados = Certificados()
        self.metrics = MetricsDashboard()
        self.widgets = DashboardWidgets(self.solicitudes, self.certificados)
        self.cache_manager = CacheManager()
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Inicializa el estado de la página"""
        if 'home_view' not in st.session_state:
            st.session_state.home_view = "general"
        if 'date_range' not in st.session_state:
            st.session_state.date_range = (
                datetime.now() - timedelta(days=30),
                datetime.now()
            )

    def render(self) -> None:
        """Renderiza la página de inicio"""
        try:
            st.title("Panel Principal ACMA")

            # Selector de vista y rango de fechas
            col1, col2 = st.columns([1, 2])
            with col1:
                view = st.radio(
                    "Vista",
                    ["General", "Detallada"],
                    horizontal=True,
                    key="home_view"
                )
            with col2:
                st.session_state.date_range = st.date_input(
                    "Rango de fechas",
                    value=st.session_state.date_range,
                    key="home_date_range"
                )

            if view == "General":
                self._render_general_view()
            else:
                self._render_detailed_view()

        except Exception as e:
            Logger.error(f"Error en página de inicio: {str(e)}")
            st.error("Error cargando el panel principal")

    def _render_general_view(self) -> None:
        """Renderiza vista general"""
        metrics = self._get_metrics_summary()

        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Solicitudes", metrics.get('total_requests', 0))
        with col2:
            st.metric("Pendientes", metrics.get('pending_requests', 0))
        with col3:
            st.metric("Certificados", metrics.get('total_certificates', 0))
        with col4:
            st.metric("Tasa de Éxito", f"{metrics.get('success_rate', 0)}%")

        # Actividad reciente
        st.header("Actividad Reciente")
        recent_data = self._get_recent_data()
        self._render_activity_timeline(recent_data)

    def _render_detailed_view(self) -> None:
        """Renderiza vista detallada"""
        # Panel de métricas completo
        self.metrics.render()

        # Análisis detallado
        st.header("Análisis Detallado")
        self._render_detailed_analysis()

    def _get_metrics_summary(self) -> Dict:
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
        if not requests:
            return 100.0
        completed = len([r for r in requests if r['status'] == 'completed'])
        return round((completed / len(requests)) * 100, 2)

    def _get_recent_data(self) -> Dict:
        """Obtiene datos recientes"""
        requests = self.solicitudes.get_requests()
        certificates = self.certificados.get_certificates()

        return {
            'requests': sorted(requests, key=lambda x: x['created_at'], reverse=True)[:10],
            'certificates': sorted(certificates, key=lambda x: x['created_at'], reverse=True)[:10]
        }

    def _render_activity_timeline(self, data: Dict) -> None:
        """Renderiza línea de tiempo de actividad"""
        fig = go.Figure()

        # Agregar solicitudes
        request_dates = [r['created_at'] for r in data['requests']]
        fig.add_trace(go.Scatter(
            x=request_dates,
            y=[1] * len(request_dates),
            name='Solicitudes',
            mode='markers'
        ))

        # Agregar certificados
        cert_dates = [c['created_at'] for c in data['certificates']]
        fig.add_trace(go.Scatter(
            x=cert_dates,
            y=[0] * len(cert_dates),
            name='Certificados',
            mode='markers'
        ))

        fig.update_layout(
            title="Línea de Tiempo de Actividad",
            showlegend=True,
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_detailed_analysis(self) -> None:
        """Renderiza análisis detallado"""
        col1, col2 = st.columns(2)

        with col1:
            self._render_provider_distribution()
        with col2:
            self._render_status_distribution()

    def _render_provider_distribution(self) -> None:
        """Renderiza distribución por proveedor"""
        providers = self.solicitudes.get_provider_stats()
        fig = px.pie(
            values=list(providers.values()),
            names=list(providers.keys()),
            title="Distribución por Proveedor"
        )
        st.plotly_chart(fig)

    def _render_status_distribution(self) -> None:
        """Renderiza distribución por estado"""
        requests = self.solicitudes.get_requests()
        status_counts = pd.DataFrame(requests)['status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Distribución por Estado"
        )
        st.plotly_chart(fig)


def render_home_page():
    """Punto de entrada para la página de inicio"""
    page = HomePage()
    page.render()
