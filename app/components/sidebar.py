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
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False

    def render(self) -> None:
        """Renderiza la barra lateral"""
        try:
            with st.sidebar:
                # Ocultar elementos no deseados
                st.markdown("""
                    <style>
                        header[data-testid="stHeader"] {display: none;}
                        div.block-container {padding-top: 0;}
                        div.stButton > button {
                            width: 100%;
                            margin-bottom: 8px;
                        }
                        div[data-testid="stSidebarNav"] {display: none !important;}
                        ul[data-testid="stSidebarNavItems"] {display: none !important;}
                        div[data-testid="stSidebarNavSeparator"] {display: none !important;}
                        .st-emotion-cache-bjn8wh {display: none !important;}
                        .st-emotion-cache-1ekxtbt {display: none !important;}
                        section[data-testid="stSidebar"] > div {
                            padding-top: 0;
                        }
                        section[data-testid="stSidebar"] button[kind="secondary"] {
                            border: none;
                            padding: 0.5rem 1rem;
                            width: 100%;
                        }
                    </style>
                """, unsafe_allow_html=True)

                if not st.session_state.authenticated:
                    # Solo mostrar el formulario de login sin navegación
                    self.auth.login_form()
                else:
                    # Menú de navegación
                    with st.container():
                        # Definir las páginas disponibles
                        pages: Dict[str, Dict] = {
                            "home": {
                                "name": "Inicio",
                                "icon": "🏠",
                                "order": 1
                            },
                            "certificates": {
                                "name": "Certificados",
                                "icon": "📜",
                                "order": 2
                            },
                            "requests": {
                                "name": "Solicitudes",
                                "icon": "📝",
                                "order": 3
                            },
                            "settings": {
                                "name": "Configuración",
                                "icon": "⚙️",
                                "order": 4
                            }
                        }

                        # Ordenar páginas
                        sorted_pages = sorted(
                            pages.items(),
                            key=lambda x: x[1]['order']
                        )

                        # Crear botones de navegación
                        for page_id, page_info in sorted_pages:
                            button_key = f"nav_{page_id}"
                            is_active = st.session_state.current_page == page_id

                            if st.button(
                                f"{page_info['icon']} {page_info['name']}",
                                key=button_key,
                                use_container_width=True,
                                type="primary" if is_active else "secondary"
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
                            st.session_state.current_page = "home"
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
