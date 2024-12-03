from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import plotly.express as px
import streamlit as st

from app.components.certificados import Certificados
from app.components.dashboard_widgets import DashboardWidgets
from app.components.solicitudes import Solicitudes
from app.utils.logger import Logger


class MetricsDashboard:
    def __init__(self):
        if not hasattr(self, '_initialized'):
            try:
                self.solicitudes = Solicitudes()
                self.certificados = Certificados()
                self.widgets = DashboardWidgets(self.solicitudes, self.certificados)
                self._initialized = True
            except Exception as e:
                Logger.error(f"Error inicializando MetricsDashboard: {str(e)}")
                raise

    def render(self) -> None:
        """Renderiza el dashboard de métricas"""
        try:
            # Métricas principales
            self.widgets.show_metrics_card()

            # Gráficos principales
            st.markdown("<br>", unsafe_allow_html=True)

            # Historial y análisis
            col1, col2 = st.columns(2)
            with col1:
                self.widgets.show_requests_timeline()
            with col2:
                self._render_service_stats()  # Reemplazamos show_provider_stats

            # Análisis detallado
            st.markdown("<br>", unsafe_allow_html=True)
            st.header("Análisis Detallado")
            self._render_detailed_analysis()

        except Exception as e:
            Logger.error(f"Error en dashboard de métricas: {str(e)}")
            st.error("Error cargando métricas")

    def _render_service_stats(self) -> None:
        """Renderiza estadísticas de servicios"""
        try:
            st.subheader("Análisis de Servicios")
            certificates = self.certificados.get_certificates()

            if not certificates:
                st.info("No hay datos disponibles")
                return

            # Contar servicios por tipo
            service_counts = {}
            for cert in certificates:
                service_type = cert.get('type', 'Otros')
                service_counts[service_type] = service_counts.get(service_type, 0) + 1

            # Crear gráfico
            fig = px.pie(
                values=list(service_counts.values()),
                names=list(service_counts.keys()),
                title="Distribución de Servicios"
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            Logger.error(f"Error mostrando estadísticas de servicios: {str(e)}")
            st.error("Error al mostrar estadísticas")

    def get_metrics_summary(self) -> Dict[str, Union[int, float]]:
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

    def _calculate_success_rate(self, requests: List[Dict[str, Any]]) -> float:
        """Calcula la tasa de éxito de las solicitudes"""
        try:
            if not requests:
                return 100.0
            completed = len([r for r in requests if r['status'] == 'completed'])
            return round((completed / len(requests)) * 100, 2)
        except Exception as e:
            Logger.error(f"Error calculando tasa de éxito: {str(e)}")
            return 0.0

    def _render_detailed_analysis(self) -> None:
        """Renderiza análisis detallado"""
        try:
            col1, col2 = st.columns(2)

            with col1:
                self._render_status_distribution()
            with col2:
                self._render_timeline_analysis()

        except Exception as e:
            Logger.error(f"Error en análisis detallado: {str(e)}")
            st.error("Error mostrando análisis detallado")

    def _render_status_distribution(self) -> None:
        """Renderiza distribución por estado"""
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
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            Logger.error(f"Error en distribución de estados: {str(e)}")
            st.error("Error mostrando distribución")

    def _render_timeline_analysis(self) -> None:
        """Renderiza análisis de línea de tiempo"""
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

            fig = px.line(
                x=list(monthly_data.keys()),
                y=list(monthly_data.values()),
                title="Tendencia Mensual de Certificaciones"
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            Logger.error(f"Error en análisis de línea de tiempo: {str(e)}")
            st.error("Error mostrando análisis temporal")
