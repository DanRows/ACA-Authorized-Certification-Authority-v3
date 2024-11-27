from datetime import datetime
from typing import Dict, List

import plotly.graph_objects as go  # type: ignore
import streamlit as st  # type: ignore

from app.components.certificados import Certificados
from app.components.solicitudes import Solicitudes
from app.utils.logger import Logger


class DashboardWidgets:
    def __init__(self, solicitudes: Solicitudes, certificados: Certificados):
        self.solicitudes = solicitudes
        self.certificados = certificados

    def show_metrics_card(self) -> None:
        try:
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
        try:
            st.subheader("Línea de Tiempo de Solicitudes")
            requests = self.solicitudes.get_requests()
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
        try:
            st.subheader("Estadísticas por Proveedor")
            providers = {
                'openai': {'requests': 0, 'success': 0},
                'vertex': {'requests': 0, 'success': 0},
                'sambanova': {'requests': 0, 'success': 0}
            }

            fig = go.Figure(data=[
                go.Bar(name='Solicitudes', x=list(providers.keys()),
                    y=[p['requests'] for p in providers.values()]),
                go.Bar(name='Exitosas', x=list(providers.keys()),
                    y=[p['success'] for p in providers.values()])
            ])
            st.plotly_chart(fig)
        except Exception as e:
            Logger.error(f"Error mostrando estadísticas: {str(e)}")
            st.error("Error al mostrar estadísticas")

    def _calculate_success_rate(self) -> float:
        try:
            requests = self.solicitudes.get_requests()
            if not requests:
                return 100.0
            completed = len([r for r in requests if r['status'] == 'completed'])
            return round((completed / len(requests)) * 100, 2)
        except Exception as e:
            Logger.error(f"Error calculando tasa de éxito: {str(e)}")
            return 0.0

    # ... resto del código ...