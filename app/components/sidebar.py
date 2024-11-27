from typing import Dict, Optional

import streamlit as st

from app.components.auth import Auth
from app.utils.logger import Logger


class Sidebar:
    def __init__(self):
        self.auth: Auth = Auth()
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Inicializa el estado de la barra lateral"""
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "home"

    def render(self) -> None:
        """Renderiza la barra lateral"""
        try:
            with st.sidebar:
                # Ocultar elementos no deseados
                st.markdown("""
                    <style>
                        [data-testid="stSidebarNav"] {display: none;}
                        div.st-emotion-cache-1ekxtbt {display: none;}
                        div.st-emotion-cache-16txtl3 {padding-top: 1rem;}
                        header[data-testid="stHeader"] {display: none;}
                    </style>
                """, unsafe_allow_html=True)

                if not st.session_state.get('authenticated', False):
                    # Solo mostrar el formulario de login
                    self.auth.login_form()
                else:
                    # Menú de navegación
                    with st.container():
                        # Definir las páginas disponibles
                        pages: Dict[str, Dict] = {
                            "home": {
                                "name": "Inicio",
                                "icon": "🏠"
                            },
                            "certificates": {
                                "name": "Certificados",
                                "icon": "📜"
                            },
                            "requests": {
                                "name": "Solicitudes",
                                "icon": "📝"
                            },
                            "settings": {
                                "name": "Configuración",
                                "icon": "⚙️"
                            }
                        }

                        # Crear botones de navegación
                        for page_id, page_info in pages.items():
                            if st.button(
                                f"{page_info['icon']} {page_info['name']}",
                                key=f"nav_{page_id}",
                                use_container_width=True,
                                type="primary" if st.session_state.current_page == page_id else "secondary"
                            ):
                                st.session_state.current_page = page_id
                                st.rerun()

                        # Separador
                        st.divider()

                        # Botón de cerrar sesión
                        if st.button(
                            "🚪 Cerrar Sesión",
                            use_container_width=True,
                            type="secondary"
                        ):
                            self.auth.logout()
                            st.rerun()

        except Exception as e:
            Logger.error(f"Error en sidebar: {str(e)}")
            # Mostrar error de forma más discreta
            st.sidebar.warning("Error en el menú de navegación")

    def _update_theme(self) -> None:
        """Actualiza el tema de la aplicación"""
        try:
            theme = st.session_state.get('theme', 'Claro')
            Logger.info(f"Tema actualizado a: {theme}")
        except Exception as e:
            Logger.error(f"Error actualizando tema: {str(e)}")
