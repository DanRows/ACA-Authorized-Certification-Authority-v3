import streamlit as st
from services.factory import ServiceFactory
from utils.logger import Logger
from datetime import datetime

class Chat:
    def __init__(self):
        self._initialize_session_state()
        self.ai_service = ServiceFactory.create_service(
            st.session_state.current_provider
        )
        
    def _initialize_session_state(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'current_provider' not in st.session_state:
            st.session_state.current_provider = "openai"
    
    def render(self):
        st.header("Asistente Virtual ACMA")
        
        # Mostrar historial de mensajes
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                st.caption(f"Enviado: {message['timestamp']}")
        
        # Input del usuario
        if prompt := st.chat_input("Escribe tu mensaje..."):
            # Agregar mensaje del usuario
            user_message = {
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.messages.append(user_message)
            
            try:
                # Procesar con IA
                response = self.ai_service.process_request({"prompt": prompt})
                
                # Agregar respuesta del asistente
                assistant_message = {
                    "role": "assistant",
                    "content": response["response"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.messages.append(assistant_message)
                
            except Exception as e:
                Logger.error(f"Error en chat: {str(e)}")
                st.error("Error procesando tu mensaje. Por favor intenta nuevamente.") 