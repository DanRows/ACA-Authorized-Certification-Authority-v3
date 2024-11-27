from datetime import datetime
from typing import Dict, List

import plotly.graph_objects as go  # type: ignore
import streamlit as st  # type: ignore

from app.components.certificados import Certificados
from app.components.solicitudes import Solicitudes
from app.utils.logger import Logger


class DashboardWidgets:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, solicitudes: Solicitudes, certificados: Certificados):
        if not self._initialized:
            try:
                self.solicitudes = solicitudes
                self.certificados = certificados
                # Agregar datos de ejemplo solo una vez
                if len(self.solicitudes.get_requests()) == 0:
                    self._add_sample_data()
                self.__class__._initialized = True
            except Exception as e:
                Logger.error(f"Error inicializando DashboardWidgets: {str(e)}")
                raise

    def _add_sample_data(self) -> None:
        """Agrega datos de ejemplo para desarrollo"""
        try:
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

    def show_metrics_card(self) -> None:
        """Muestra tarjeta de métricas principales"""
        try:
            # Asegurarse de que haya datos
            if len(self.solicitudes.get_requests()) == 0:
                self._add_sample_data()

            col1, col2, col3 = st.columns(3)

            with col1:
                total_requests = len(self.solicitudes.get_requests())
                st.metric("Total Solicitudes", total_requests)

            with col2:
                pending_requests = len([r for r in self.solicitudes.get_requests()
                                    if r['status'] == 'pending'])
                st.metric("Solicitudes Pendientes", pending_requests)

            with col3:
                success_rate = self._calculate_success_rate()
                st.metric("Tasa de Éxito", f"{success_rate}%")
        except Exception as e:
            Logger.error(f"Error mostrando métricas: {str(e)}")
            st.error("Error al mostrar métricas")

    def show_requests_timeline(self) -> None:
        """Muestra línea de tiempo de solicitudes"""
        try:
            st.subheader("Línea de Tiempo de Solicitudes")
            requests = self.solicitudes.get_requests()

            if not requests:
                st.info("No hay solicitudes para mostrar")
                return

            dates = [r.get('created_at', datetime.now()) for r in requests]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=range(len(dates)),
                mode='lines+markers',
                name='Solicitudes'
            ))
            st.plotly_chart(fig)
        except Exception as e:
            Logger.error(f"Error mostrando línea de tiempo: {str(e)}")
            st.error("Error al mostrar línea de tiempo")

    def show_provider_stats(self) -> None:
        """Muestra estadísticas por proveedor"""
        try:
            st.subheader("Estadísticas por Proveedor")
            providers = self.solicitudes.get_provider_stats()

            if not providers:
                st.info("No hay datos de proveedores para mostrar")
                return

            fig = go.Figure(data=[
                go.Bar(
                    name='Solicitudes',
                    x=list(providers.keys()),
                    y=list(providers.values())
                )
            ])

            fig.update_layout(
                title="Solicitudes por Proveedor",
                xaxis_title="Proveedor",
                yaxis_title="Cantidad",
                showlegend=True
            )

            st.plotly_chart(fig)
        except Exception as e:
            Logger.error(f"Error mostrando estadísticas: {str(e)}")
            st.error("Error al mostrar estadísticas")

    def _calculate_success_rate(self) -> float:
        """Calcula la tasa de éxito de las solicitudes"""
        try:
            requests = self.solicitudes.get_requests()
            if not requests:
                return 0.0
            completed = len([r for r in requests if r['status'] == 'completed'])
            return round((completed / len(requests)) * 100, 2)
        except Exception as e:
            Logger.error(f"Error calculando tasa de éxito: {str(e)}")
            return 0.0

    # ... resto del código ...
