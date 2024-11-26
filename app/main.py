import streamlit as st
from datetime import datetime
from config.configuration import Configuration
from services.factory import ServiceFactory
from components.certificados import Certificados
from components.solicitudes import Solicitudes
from utils.helpers import validate_input, get_database_connection
from functools import wraps
from utils.logger import Logger
from components.notifications import Notifications

class ACMADashboard:
    def __init__(self):
        self.config = Configuration()
        self.certificados = Certificados()
        self.solicitudes = Solicitudes()
        self.setup_session_state()
        
    def setup_session_state(self):
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'current_provider' not in st.session_state:
            st.session_state.current_provider = self.config.get_setting("default_provider")
            
    def render_sidebar(self):
        with st.sidebar:
            st.title("Configuración")
            providers = self.config.get_setting("ai_providers")
            st.session_state.current_provider = st.selectbox(
                "Proveedor de IA",
                providers,
                index=providers.index(st.session_state.current_provider)
            )
            
    def render_certificate_section(self):
        st.header("Generador de Certificados")
        with st.form("certificate_form"):
            user_data = {
                "name": st.text_input("Nombre"),
                "email": st.text_input("Email"),
                "type": st.selectbox("Tipo de Certificado", ["Básico", "Premium"])
            }
            submitted = st.form_submit_button("Generar Certificado")
            
            if submitted and validate_input(user_data, {
                "name": {"type": str},
                "email": {"type": str}
            }):
                cert = self.certificados.generate_certificate(user_data)
                st.success(cert)
                
    def render_requests_section(self):
        st.header("Gestión de Solicitudes")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Nueva Solicitud"):
                result = self.solicitudes.add_request(
                    {"timestamp": datetime.now()},
                    "certificate"
                )
                st.success(f"Solicitud creada: {result['request_id']}")
                
        with col2:
            if st.button("Ver Solicitudes"):
                requests = self.solicitudes.get_requests()
                st.json(requests)

class ErrorBoundary:
    @staticmethod
    def handle_error(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                Logger.error(f"Error en {func.__name__}: {str(e)}")
                notifications = Notifications()
                notifications.add_notification(
                    f"Error: {str(e)}",
                    type="error"
                )
                st.error("Ha ocurrido un error. Por favor, intente nuevamente.")
                return None
        return wrapper
    
    @staticmethod
    def render_error_page(error):
        st.title("¡Ups! Algo salió mal")
        
        st.error(f"""
        Ha ocurrido un error inesperado:
        
        {str(error)}
        
        Por favor, intente:
        1. Recargar la página
        2. Limpiar la caché del navegador
        3. Contactar al soporte técnico
        """)
        
        if st.button("Volver al Inicio"):
            st.experimental_rerun()

def main():
    st.set_page_config(
        page_title="ACMA Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    dashboard = ACMADashboard()
    dashboard.render_sidebar()
    
    tab1, tab2 = st.tabs(["Certificados", "Solicitudes"])
    
    with tab1:
        dashboard.render_certificate_section()
    
    with tab2:
        dashboard.render_requests_section()

if __name__ == "__main__":
    main()