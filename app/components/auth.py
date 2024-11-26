import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Optional
from utils.logger import Logger
from utils.cache import cached
from config.configuration import Configuration

class Auth:
    def __init__(self):
        self.config = Configuration()
        self._initialize_state()
    
    def _initialize_state(self):
        """Inicializa el estado de autenticación"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
    
    def login_form(self):
        """Renderiza el formulario de inicio de sesión"""
        try:
            st.header("Iniciar Sesión")
            
            with st.form("login_form"):
                username = st.text_input("Usuario")
                password = st.text_input("Contraseña", type="password")
                submitted = st.form_submit_button("Ingresar")
                
                if submitted:
                    self._handle_login(username, password)
            
            if st.session_state.login_attempts >= 3:
                st.error("Demasiados intentos fallidos. Espere 5 minutos.")
                
        except Exception as e:
            Logger.error(f"Error en formulario de login: {str(e)}")
            st.error("Error en el inicio de sesión")
    
    def logout(self):
        """Cierra la sesión del usuario"""
        if st.button("Cerrar Sesión"):
            self._clear_session()
            st.experimental_rerun()
    
    @cached(expire_in=300)
    def _validate_credentials(self, username: str, password: str) -> Optional[str]:
        """Valida credenciales con caché"""
        try:
            users = self.config.get_setting('users')
            if username in users and users[username]['password'] == password:
                return users[username]['role']
            return None
            
        except Exception as e:
            Logger.error(f"Error validando credenciales: {str(e)}")
            return None