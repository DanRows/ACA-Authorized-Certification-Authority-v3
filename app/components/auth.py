import streamlit as st
from datetime import datetime, timedelta
from utils.helpers import validate_input
from utils.logger import Logger

class Auth:
    def __init__(self):
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
            
    def login_form(self):
        st.sidebar.header("Iniciar Sesión")
        
        with st.sidebar.form("login_form"):
            credentials = {
                "username": st.text_input("Usuario"),
                "password": st.text_input("Contraseña", type="password")
            }
            
            submitted = st.form_submit_button("Ingresar")
            
            if submitted:
                if self._validate_credentials(credentials):
                    st.session_state.authenticated = True
                    st.session_state.user_role = self._get_user_role(credentials["username"])
                    st.experimental_rerun()
                else:
                    st.error("Credenciales inválidas")
    
    def logout(self):
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.experimental_rerun()
    
    def _validate_credentials(self, credentials):
        # Aquí iría la validación real contra la base de datos
        return credentials["username"] == "admin" and credentials["password"] == "admin"
    
    def _get_user_role(self, username):
        # Aquí iría la lógica real para obtener el rol del usuario
        return "admin" if username == "admin" else "user" 