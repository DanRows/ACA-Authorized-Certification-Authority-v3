import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.metrics import Metrics
from datetime import datetime, timedelta

class MetricsDashboard:
    def __init__(self):
        self.metrics = Metrics()
    
    def render(self):
        st.header("Panel de Métricas")
        
        # Selector de período
        period = st.selectbox(
            "Período",
            ["7 días", "30 días", "90 días"],
            index=1
        )
        
        days = int(period.split()[0])
        
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_requests_chart(days)
        
        with col2:
            self._render_providers_chart()
            
        # Métricas adicionales
        self._render_performance_metrics()
    
    def _render_requests_chart(self, days):
        metrics = self.metrics.get_request_metrics(days)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=metrics['dates'],
            y=metrics['daily_totals'],
            name="Total Solicitudes"
        ))
        fig.add_trace(go.Scatter(
            x=metrics['dates'],
            y=metrics['daily_completed'],
            name="Completadas"
        ))
        
        st.plotly_chart(fig)
    
    def _render_providers_chart(self):
        provider_stats = self.metrics.get_provider_stats()
        
        if provider_stats:
            fig = px.pie(
                values=[stat['total_requests'] for stat in provider_stats],
                names=[stat['provider'] for stat in provider_stats],
                title="Distribución por Proveedor"
            )
            st.plotly_chart(fig)
    
    def _render_performance_metrics(self):
        st.subheader("Métricas de Rendimiento")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Tiempo Promedio de Respuesta",
                "2.3s",
                delta="-0.5s"
            )
        
        with col2:
            st.metric(
                "Tasa de Éxito",
                "98.5%",
                delta="1.2%"
            )
            
        with col3:
            st.metric(
                "Solicitudes/Hora",
                "127",
                delta="12"
            ) 