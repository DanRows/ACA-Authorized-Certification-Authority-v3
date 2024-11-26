import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
from utils.logger import Logger
from utils.cache import cached
from services.factory import ServiceFactory

class Chat:
    def __init__(self):
        self.service_factory = ServiceFactory()
        self._initialize_state()
    
    def _initialize_state(self):
        """Inicializa el estado del chat"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_provider' not in st.session_state:
            st.session_state.current_provider = "openai"
    
    def render(self):
        """Renderiza la interfaz del chat"""
        try:
            st.title("Chat de Asistencia")
            
            # Selector de proveedor
            providers = self.service_factory.get_available_providers()
            st.session_state.current_provider = st.selectbox(
                "Proveedor de IA",
                options=providers,
                index=providers.index(st.session_state.current_provider)
            )
            
            # Historial del chat
            self._render_chat_history()
            
            # Input del usuario
            with st.form("chat_input", clear_on_submit=True):
                user_input = st.text_area("Mensaje", height=100)
                submitted = st.form_submit_button("Enviar")
                
                if submitted and user_input:
                    self._handle_user_input(user_input)
            
        except Exception as e:
            Logger.error(f"Error en chat: {str(e)}")
            st.error("Error en el chat")
    
    def _render_chat_history(self):
        """Renderiza el historial del chat"""
        st.subheader("Conversación")
        
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                st.caption(f"via {message['provider']} - {message['timestamp']}")
    
    @cached(expire_in=60)
    def _get_ai_response(self, message: str, provider: str) -> str:
        """Obtiene respuesta del modelo con caché"""
        try:
            service = self.service_factory.get_service(provider)
            return service.get_completion(message)
        except Exception as e:
            Logger.error(f"Error obteniendo respuesta: {str(e)}")
            return "Lo siento, hubo un error procesando tu mensaje."