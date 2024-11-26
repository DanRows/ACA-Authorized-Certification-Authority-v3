import streamlit as st
from datetime import datetime
from typing import Dict, Optional, List
from config.configuration import Configuration
from config.secrets_manager import SecretsManager
from utils.logger import Logger
from utils.cache import cached
from components.notifications import Notifications

class SettingsPage:
    def __init__(self):
        self.config = Configuration()
        self.secrets = SecretsManager()
        self.notifications = Notifications()
        self._initialize_state()
    
    def _initialize_state(self):
        """Inicializa el estado de la página"""
        if 'settings_modified' not in st.session_state:
            st.session_state.settings_modified = False
        if 'current_tab' not in st.session_state:
            st.session_state.current_tab = 0
    
    def render(self):
        """Renderiza la página de configuración"""
        try:
            st.title("Configuración del Sistema")
            
            # Tabs para diferentes secciones
            tabs = ["Proveedores IA", "Base de Datos", "Rendimiento", "Notificaciones"]
            current_tab = st.tabs(tabs)
            
            with current_tab[0]:
                self._render_ai_settings()
            with current_tab[1]:
                self._render_database_settings()
            with current_tab[2]:
                self._render_performance_settings()
            with current_tab[3]:
                self._render_notification_settings()
            
            # Botón de guardar cambios
            if st.session_state.settings_modified:
                self._render_save_button()
                
        except Exception as e:
            Logger.error(f"Error en página de configuración: {str(e)}")
            st.error("Error cargando configuración")
    
    @cached(expire_in=300)
    def _get_settings(self) -> Dict:
        """Obtiene configuraciones con caché"""
        return {
            'ai_providers': self.config.get_setting('ai_providers'),
            'database': self.config.get_setting('database'),
            'performance': self.config.get_setting('performance'),
            'notifications': self.config.get_setting('notifications')
        }
    
    def _render_ai_settings(self):
        """Renderiza configuración de proveedores IA"""
        st.header("Configuración de Proveedores IA")
        
        settings = self._get_settings()
        providers = settings.get('ai_providers', {})
        
        for provider, config in providers.items():
            with st.expander(f"Configuración de {provider}"):
                api_key = st.text_input(
                    "API Key",
                    type="password",
                    value=config.get('api_key', ''),
                    key=f"api_key_{provider}"
                )
                
                model = st.selectbox(
                    "Modelo",
                    options=config.get('available_models', []),
                    index=0,
                    key=f"model_{provider}"
                )
                
                max_tokens = st.number_input(
                    "Máximo de tokens",
                    min_value=1,
                    max_value=4096,
                    value=config.get('max_tokens', 2048),
                    key=f"max_tokens_{provider}"
                )
    
    def _render_database_settings(self):
        """Renderiza configuración de base de datos"""
        st.header("Configuración de Base de Datos")
        
        with st.form("database_config"):
            db_url = st.text_input(
                "URL de Base de Datos",
                value=self.config.get_setting("database_url"),
                type="password"
            )
            
            if st.form_submit_button("Actualizar Configuración"):
                try:
                    # Aquí iría la lógica para actualizar la configuración
                    st.success("Configuración actualizada exitosamente")
                except Exception as e:
                    st.error(f"Error: {str(e)}") 