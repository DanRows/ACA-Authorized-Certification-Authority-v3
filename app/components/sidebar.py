import base64
from pathlib import Path
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

    def _get_logo_base64(self) -> str:
        """Obtiene el logo en formato base64"""
        try:
            # Obtener la ruta absoluta del logo desde assets
            logo_path = Path(__file__).parent.parent.parent / "assets" / "procymi_logo.png"

            # Depurar la ruta
            Logger.info(f"Buscando logo en: {logo_path}")
            Logger.info(f"¿La ruta existe?: {logo_path.exists()}")

            if not logo_path.exists():
                Logger.warning(f"Logo no encontrado en: {logo_path}")
                return ""

            # Leer y codificar el logo
            with open(logo_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                Logger.info("Logo cargado y codificado exitosamente")
                return encoded

        except Exception as e:
            Logger.error(f"Error cargando logo: {str(e)}")
            return ""

    def render(self) -> None:
        """Renderiza la barra lateral"""
        try:
            with st.sidebar:
                # Ocultar elementos no deseados y estilizar
                logo_base64 = self._get_logo_base64()
                style_html = """
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
                        /* Estilos del logo */
                        .logo-container {
                            display: flex;
                            justify-content: center;
                            padding: 1rem 0;
                            margin-bottom: 2rem;
                        }
                        .logo-container img {
                            max-width: 150px;
                            height: auto;
                        }
                    </style>
                """
                st.markdown(style_html, unsafe_allow_html=True)

                # Cargar y mostrar el logo
                if logo_base64:
                    st.markdown(
                        f"""
                        <div class="logo-container">
                            <img src="data:image/png;base64,{logo_base64}"
                                 alt="PROCyMI Logo"
                                 style="max-width: 150px; height: auto;"/>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    Logger.warning("No se pudo cargar el logo")

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
                            "clients": {
                                "name": "Clientes",
                                "icon": "👥",
                                "order": 2
                            },
                            "certificates": {
                                "name": "Certificados",
                                "icon": "📜",
                                "order": 3
                            },
                            "requests": {
                                "name": "Solicitudes",
                                "icon": "📝",
                                "order": 4
                            },
                            "settings": {
                                "name": "Configuración",
                                "icon": "⚙️",
                                "order": 5
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
