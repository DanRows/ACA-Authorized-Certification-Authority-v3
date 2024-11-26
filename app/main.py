import streamlit as st
from datetime import datetime
from typing import Dict, List
import plotly.graph_objects as go
import plotly.express as px

from config.configuration import Configuration
from services.factory import ServiceFactory
from components.certificados import Certificados
from components.solicitudes import Solicitudes
from components.auth import Auth
from components.chat import Chat
from components.notifications import Notifications
from components.metrics_dashboard import MetricsDashboard
from components.sidebar import Sidebar
from components.report_generator import ReportGenerator
from utils.helpers import validate_input, get_database_connection
from utils.logger import Logger
from utils.cache import cached

class ACMADashboard:
    def __init__(self):
        self.config = Configuration()
        self.auth = Auth()
        self.certificados = Certificados()
        self.solicitudes = Solicitudes()
        self.chat = Chat()
        self.notifications = Notifications()
        self.metrics = MetricsDashboard()
        self.report_generator = ReportGenerator()
        self.sidebar = Sidebar()
        self.setup_session_state()
        
    def setup_session_state(self):
        """Inicializa el estado de la sesión con valores predeterminados"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'current_provider' not in st.session_state:
            st.session_state.current_provider = self.config.get_setting("default_provider")
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "home"
            
    @cached(expire_in=300)  # Cache por 5 minutos
    def render_metrics_dashboard(self):
        """Renderiza el panel de métricas con caché"""
        self.metrics.render()
            
    def render_content(self):
        """Renderiza el contenido principal según la página actual"""
        if not st.session_state.authenticated:
            st.warning("Por favor inicia sesión para acceder al dashboard")
            return
            
        pages = {
            "home": self.render_home,
            "certificates": self.render_certificate_section,
            "requests": self.render_requests_section,
            "chat": self.chat.render,
            "metrics": self.render_metrics_dashboard,
            "reports": self.report_generator.render
        }
        
        current_page = st.session_state.current_page
        if current_page in pages:
            pages[current_page]()
        else:
            st.error("Página no encontrada")
    
    def render_home(self):
        """Renderiza la página de inicio"""
        st.title("ACMA Dashboard - Panel Principal")
        
        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1:
            total_requests = len(self.solicitudes.get_requests())
            st.metric("Total Solicitudes", total_requests)
        with col2:
            pending = len([r for r in self.solicitudes.get_requests() if r['status'] == 'pending'])
            st.metric("Pendientes", pending)
        with col3:
            success_rate = self._calculate_success_rate()
            st.metric("Tasa de Éxito", f"{success_rate}%")
            
        # Gráficos y estadísticas
        self._render_statistics()
    
    def _render_statistics(self):
        """Renderiza gráficos y estadísticas"""
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_requests_timeline()
        with col2:
            self._render_provider_distribution()
    
    def _render_requests_timeline(self):
        """Renderiza la línea de tiempo de solicitudes"""
        st.subheader("Actividad Reciente")
        requests = self.solicitudes.get_requests()
        if requests:
            dates = [r['created_at'] for r in requests]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=range(len(dates))))
            st.plotly_chart(fig)
        else:
            st.info("No hay solicitudes registradas")
    
    def _render_provider_distribution(self):
        """Renderiza la distribución de uso por proveedor"""
        st.subheader("Distribución por Proveedor")
        providers = ServiceFactory.get_available_providers()
        values = [1] * len(providers)  # Simulado
        fig = px.pie(values=values, names=providers)
        st.plotly_chart(fig)
    
    def _calculate_success_rate(self) -> float:
        """Calcula la tasa de éxito de las solicitudes"""
        requests = self.solicitudes.get_requests()
        if not requests:
            return 100.0
        completed = len([r for r in requests if r['status'] == 'completed'])
        return round((completed / len(requests)) * 100, 2)

def main():
    """Función principal de la aplicación"""
    st.set_page_config(
        page_title="ACMA Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    try:
        dashboard = ACMADashboard()
        dashboard.sidebar.render()
        dashboard.render_content()
        
    except Exception as e:
        Logger.error(f"Error crítico en la aplicación: {str(e)}")
        st.error("""
        Ha ocurrido un error inesperado. 
        Por favor, intente:
        1. Recargar la página
        2. Limpiar la caché del navegador
        3. Contactar al soporte técnico
        """)

if __name__ == "__main__":
    main()