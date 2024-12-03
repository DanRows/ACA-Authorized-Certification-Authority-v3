from datetime import datetime, timedelta

import plotly.express as px
import streamlit as st

from app.components.certificados import Certificados
from app.components.solicitudes import Solicitudes
from app.utils.logger import Logger


class MetricsDashboard:
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
                # Agregar datos de ejemplo solo una vez
                self._add_sample_data()
                self.__class__._initialized = True
            except Exception as e:
                Logger.error(f"Error inicializando MetricsDashboard: {str(e)}")
                raise

    def _add_sample_data(self) -> None:
        """Agrega datos de ejemplo para desarrollo"""
        try:
            # Verificar si ya hay datos
            if len(self.solicitudes.get_requests()) == 0:
                # Agregar algunas solicitudes de ejemplo
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
                # Agregar algunos certificados de ejemplo
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
        """Renderiza el dashboard de métricas"""
        try:
            # Asegurarse de que haya datos
            if len(self.solicitudes.get_requests()) == 0:
                self._add_sample_data()

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
            if not providers:
                st.info("No hay datos de proveedores para mostrar")
                return

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
            if not requests:
                st.info("No hay datos de estados para mostrar")
                return

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
