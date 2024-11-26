import streamlit as st
from components.dashboard_widgets import DashboardWidgets
from components.certificados import Certificados
from components.solicitudes import Solicitudes
from utils.logger import Logger

def render_home():
    st.title("ACMA Dashboard - Inicio")
    
    certificados = Certificados()
    solicitudes = Solicitudes()
    widgets = DashboardWidgets(solicitudes, certificados)
    
    # Métricas principales
    widgets.show_metrics_card()
    
    # Secciones principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Últimas Solicitudes")
        recent_requests = solicitudes.get_requests(limit=5)
        for req in recent_requests:
            st.info(
                f"Solicitud #{req['id']} - {req['type']}\n"
                f"Estado: {req['status']}"
            )
            
    with col2:
        st.header("Certificados Recientes")
        recent_certs = certificados.get_recent_certificates(limit=5)
        for cert in recent_certs:
            st.success(
                f"Certificado para: {cert['user_data']['name']}\n"
                f"Fecha: {cert['created_at']}"
            ) 