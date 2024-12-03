from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.components.certificados import Certificados
from app.components.metrics_dashboard import MetricsDashboard
from app.components.solicitudes import Solicitudes
from app.utils.cache import CacheManager
from app.utils.logger import Logger


class HomePage:
    def __init__(self):
        self.solicitudes = Solicitudes()
        self.certificados = Certificados()
        self.metrics = MetricsDashboard()
        self.cache_manager = CacheManager()
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Inicializa el estado de la página"""
        if 'home_view' not in st.session_state:
            st.session_state.home_view = "General"
        if 'date_range' not in st.session_state:
            st.session_state.date_range = [
                datetime.now() - timedelta(days=30),
                datetime.now()
            ]

    def render(self) -> None:
        """Renderiza la página de inicio"""
        try:
            # Selector de vista
            col1, col2 = st.columns([3, 1])
            with col1:
                view_options = ["General", "Detallado"]
                current_view = st.session_state.home_view
                selected_view = st.radio(
                    "Vista",
                    options=view_options,
                    index=view_options.index(current_view),
                    horizontal=True,
                    key="home_view_radio"
                )
                st.session_state.home_view = selected_view

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
            # Panel de métricas
            self.metrics.render()

        except Exception as e:
            Logger.error(f"Error en vista general: {str(e)}")
            st.error("Error cargando vista general")

    def _render_detailed_view(self) -> None:
        """Renderiza vista detallada"""
        try:
            # Análisis detallado
            st.header("Análisis Detallado")

            # Métricas detalladas
            metrics = self.metrics.get_metrics_summary()

            # Mostrar métricas en columnas
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Solicitudes",
                    metrics.get('total_requests', 0)
                )
            with col2:
                st.metric(
                    "Pendientes",
                    metrics.get('pending_requests', 0)
                )
            with col3:
                st.metric(
                    "Total Certificados",
                    metrics.get('total_certificates', 0)
                )
            with col4:
                st.metric(
                    "Tasa de Éxito",
                    f"{metrics.get('success_rate', 0)}%"
                )

            # Gráficos detallados
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_detailed_charts()

        except Exception as e:
            Logger.error(f"Error en vista detallada: {str(e)}")
            st.error("Error cargando vista detallada")

    def _render_detailed_charts(self) -> None:
        """Renderiza gráficos detallados"""
        try:
            col1, col2 = st.columns(2)

            with col1:
                self._render_timeline_chart()
            with col2:
                self._render_status_chart()

        except Exception as e:
            Logger.error(f"Error en gráficos detallados: {str(e)}")
            st.error("Error cargando gráficos")

    def _render_timeline_chart(self) -> None:
        """Renderiza gráfico de línea de tiempo"""
        try:
            certificates = self.certificados.get_certificates()
            if not certificates:
                st.info("No hay datos disponibles")
                return

            # Agrupar por mes
            monthly_data = {}
            for cert in certificates:
                month = cert['created_at'].strftime('%Y-%m')
                monthly_data[month] = monthly_data.get(month, 0) + 1

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(monthly_data.keys()),
                y=list(monthly_data.values()),
                mode='lines+markers',
                name='Certificaciones'
            ))
            fig.update_layout(
                title="Certificaciones por Mes",
                xaxis_title="Mes",
                yaxis_title="Cantidad",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            Logger.error(f"Error en gráfico de línea de tiempo: {str(e)}")
            st.error("Error mostrando gráfico")

    def _render_status_chart(self) -> None:
        """Renderiza gráfico de estados"""
        try:
            certificates = self.certificados.get_certificates()
            if not certificates:
                st.info("No hay datos disponibles")
                return

            status_counts = {}
            for cert in certificates:
                status = cert.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1

            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Estado de Certificaciones"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            Logger.error(f"Error en gráfico de estados: {str(e)}")
            st.error("Error mostrando gráfico")


def render_home_page():
    """Punto de entrada para la página de inicio"""
    try:
        page = HomePage()
        page.render()
    except Exception as e:
        Logger.error(f"Error en render_home_page: {str(e)}")
        st.error("Error cargando la página de inicio")
