import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.logger import Logger
from utils.cache import cached
from components.solicitudes import Solicitudes
from components.certificados import Certificados

class MetricsDashboard:
    def __init__(self):
        self.solicitudes = Solicitudes()
        self.certificados = Certificados()
        self._initialize_state()
    
    def _initialize_state(self):
        """Inicializa el estado del dashboard"""
        if 'metrics_period' not in st.session_state:
            st.session_state.metrics_period = 30
        if 'metrics_cache' not in st.session_state:
            st.session_state.metrics_cache = {}
    
    def render(self):
        """Renderiza el dashboard de métricas"""
        try:
            st.title("Panel de Métricas")
            
            # Selector de período
            days = st.slider(
                "Período de análisis (días)",
                min_value=7,
                max_value=90,
                value=st.session_state.metrics_period
            )
            
            # Métricas principales
            self._render_main_metrics(days)
            
            # Gráficos detallados
            self._render_detailed_charts(days)
            
        except Exception as e:
            Logger.error(f"Error en dashboard de métricas: {str(e)}")
            st.error("Error cargando métricas")
    
    @cached(expire_in=300)
    def _get_metrics_data(self, days: int) -> Dict:
        """Obtiene datos de métricas con caché"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return {
            'daily_requests': self._get_daily_metrics(
                self.solicitudes.get_requests(),
                start_date,
                end_date
            ),
            'daily_certificates': self._get_daily_metrics(
                self.certificados.get_certificates(),
                start_date,
                end_date
            ),
            'success_rate': self._calculate_success_rate(days)
        }
    
    def _render_main_metrics(self, days: int):
        """Renderiza métricas principales"""
        metrics = self._get_metrics_data(days)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_requests = sum(metrics['daily_requests'].values())
            st.metric(
                "Total Solicitudes",
                f"{total_requests:,}",
                help="Total de solicitudes en el período"
            )
        
        with col2:
            total_certs = sum(metrics['daily_certificates'].values())
            st.metric(
                "Certificados Generados",
                f"{total_certs:,}",
                help="Total de certificados generados"
            )
        
        with col3:
            st.metric(
                "Tasa de Éxito",
                f"{metrics['success_rate']:.1f}%",
                help="Porcentaje de solicitudes exitosas"
            )
    
    def _render_detailed_charts(self, days: int):
        """Renderiza gráficos detallados"""
        metrics = self._get_metrics_data(days)
        
        # Gráfico de tendencias
        self._render_trends_chart(metrics)
        
        # Distribución por tipo
        self._render_distribution_chart(metrics)
    
    def _render_trends_chart(self, metrics: Dict):
        """Renderiza gráfico de tendencias"""
        df = pd.DataFrame({
            'Fecha': list(metrics['daily_requests'].keys()),
            'Solicitudes': list(metrics['daily_requests'].values()),
            'Certificados': list(metrics['daily_certificates'].values())
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Fecha'],
            y=df['Solicitudes'],
            name='Solicitudes',
            mode='lines'
        ))
        fig.add_trace(go.Scatter(
            x=df['Fecha'],
            y=df['Certificados'],
            name='Certificados',
            mode='lines'
        ))
        
        st.plotly_chart(fig)