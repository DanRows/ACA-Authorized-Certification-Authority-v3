import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from components.dashboard_widgets import DashboardWidgets
from components.certificados import Certificados
from components.solicitudes import Solicitudes
from components.metrics_dashboard import MetricsDashboard
from utils.logger import Logger
from utils.cache import cached

class HomePage:
    def __init__(self):
        self.solicitudes = Solicitudes()
        self.certificados = Certificados()
        self.metrics = MetricsDashboard()
        self.widgets = DashboardWidgets(self.solicitudes, self.certificados)
        self._initialize_state()
    
    def _initialize_state(self):
        """Inicializa el estado de la página"""
        if 'home_view' not in st.session_state:
            st.session_state.home_view = "general"
        if 'date_range' not in st.session_state:
            st.session_state.date_range = (
                datetime.now() - timedelta(days=30),
                datetime.now()
            )
    
    def render(self):
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
    
    @cached(expire_in=300)
    def _get_metrics_summary(self) -> Dict:
        """Obtiene resumen de métricas con caché"""
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
    
    def _render_general_view(self):
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
    
    def _render_detailed_view(self):
        """Renderiza vista detallada"""
        # Panel de métricas completo
        self.metrics.render()
        
        # Análisis detallado
        st.header("Análisis Detallado")
        self._render_detailed_analysis()
    
    @cached(expire_in=300)
    def _get_recent_data(self) -> Dict:
        """Obtiene datos recientes con caché"""
        return {
            'requests': self.solicitudes.get_requests(limit=10),
            'certificates': self.certificados.get_certificates(limit=10)
        }
    
    def _render_activity_timeline(self, data: Dict):
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