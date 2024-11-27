from typing import Optional

import streamlit as st

from app.components.auth import Auth
from app.utils.logger import Logger


class Sidebar:
    def __init__(self):
        self.auth: Auth = Auth()

    def render(self) -> None:
        """Renderiza la barra lateral"""
        try:
            with st.sidebar:
                if not st.session_state.get('authenticated', False):
                    self.auth.login_form()
                else:
                    st.title("ACMA Dashboard")

                    # Agregar selector de tema
                    st.selectbox(
                        "Tema",
                        ["Claro", "Oscuro"],
                        key="theme",
                        on_change=self._update_theme
                    )

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
                            st.rerun()

                    # Botón de cerrar sesión
                    self.auth.logout()
        except Exception as e:
            Logger.error(f"Error en sidebar: {str(e)}")
            st.error("Error cargando la barra lateral")

    def _update_theme(self):
        # Lógica para actualizar el tema aquí
        pass
