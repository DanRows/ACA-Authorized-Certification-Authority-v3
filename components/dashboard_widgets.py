from datetime import datetime
from typing import Dict, List

import plotly.graph_objects as go
import streamlit as st

from components.certificados import Certificados
from components.solicitudes import Solicitudes
from utils.logger import Logger


class DashboardWidgets:
    def __init__(self, solicitudes: Solicitudes, certificados: Certificados):
        self.solicitudes = solicitudes
        self.certificados = certificados

    def show_metrics_card(self) -> None:
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

    def show_requests_timeline(self) -> None:
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

    def show_provider_stats(self) -> None:
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

    def _calculate_success_rate(self) -> float:
        requests = self.solicitudes.get_requests()
        if not requests:
            return 100.0
        completed = len([r for r in requests if r['status'] == 'completed'])
        return round((completed / len(requests)) * 100, 2)
