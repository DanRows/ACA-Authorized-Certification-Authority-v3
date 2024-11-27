from datetime import datetime
from typing import Dict, List, Optional

import streamlit as st

from app.services.factory import ServiceFactory
from app.utils.cache import cached
from app.utils.logger import Logger


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
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                st.caption(f"via {message['provider']} - {message['timestamp']}")

    def _handle_user_input(self, user_input: str):
        """Maneja la entrada del usuario"""
        try:
            # Agregar mensaje del usuario al historial
            self._add_message("user", user_input)

            # Obtener respuesta del modelo
            response = self._get_ai_response(user_input)

            # Agregar respuesta al historial
            self._add_message("assistant", response)

        except Exception as e:
            Logger.error(f"Error procesando mensaje: {str(e)}")
            st.error("Error procesando tu mensaje")

    def _add_message(self, role: str, content: str):
        """Agrega un mensaje al historial"""
        st.session_state.chat_history.append({
            "role": role,
            "content": content,
            "provider": st.session_state.current_provider,
            "timestamp": datetime.now().strftime("%H:%M")
        })

    @cached(ttl=60)
    def _get_ai_response(self, message: str) -> str:
        """Obtiene respuesta del modelo con caché"""
        try:
            service = self.service_factory.get_service(st.session_state.current_provider)
            return service.get_completion(message)
        except Exception as e:
            Logger.error(f"Error obteniendo respuesta: {str(e)}")
            return "Lo siento, hubo un error procesando tu mensaje."
