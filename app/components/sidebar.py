import streamlit as st
from components.auth import Auth

class Sidebar:
    def __init__(self):
        self.auth = Auth()
    
    def render(self):
        with st.sidebar:
            if not st.session_state.authenticated:
                self.auth.login_form()
            else:
                st.title("ACMA Dashboard")
                st.write(f"Usuario: {st.session_state.user_role}")
                
                # Menú de navegación
                st.header("Navegación")
                
                pages = {
                    "Inicio": "home",
                    "Certificados": "certificates",
                    "Solicitudes": "requests",
                    "Configuración": "settings"
                }
                
                for page_name, page_id in pages.items():
                    if st.button(page_name):
                        st.session_state.current_page = page_id
                        st.experimental_rerun()
                
                # Botón de cerrar sesión
                self.auth.logout() 