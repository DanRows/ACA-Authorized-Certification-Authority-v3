from datetime import datetime
from typing import Dict, List, Optional

import streamlit as st

from app.components.certificados import Certificados
from app.utils.logger import Logger


class CertificatesPage:
    def __init__(self):
        self.certificados = Certificados()
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Inicializa el estado de la página"""
        if 'certificates_filter' not in st.session_state:
            st.session_state.certificates_filter = "all"

    def render(self) -> None:
        """Renderiza la página de certificados"""
        try:
            st.title("Gestión de Certificados")

            # Filtros
            self._render_filters()

            # Lista de certificados
            self._render_certificates_list()

        except Exception as e:
            Logger.error(f"Error en página de certificados: {str(e)}")
            st.error("Error cargando certificados")

    def _render_filters(self) -> None:
        """Renderiza filtros de certificados"""
        st.session_state.certificates_filter = st.selectbox(
            "Estado",
            ["all", "pending", "active", "expired"],
            format_func=lambda x: {
                "all": "Todos",
                "pending": "Pendientes",
                "active": "Activos",
                "expired": "Expirados"
            }[x]
        )

    def _render_certificates_list(self) -> None:
        """Renderiza lista de certificados"""
        certificates = self.certificados.get_certificates()

        if not certificates:
            st.info("No hay certificados disponibles")
            return

        for cert in certificates:
            with st.expander(f"Certificado {cert['id']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Fecha: {cert['created_at']}")
                    st.write(f"Estado: {cert.get('status', 'N/A')}")
                with col2:
                    if cert.get('details'):
                        st.json(cert['details'])

                # Acciones
                if cert['status'] == 'pending':
                    if st.button("Activar", key=f"activate_{cert['id']}"):
                        self.certificados.update_certificate(
                            cert['id'],
                            {"status": "active"}
                        )
                        st.success("Certificado activado")
                        st.rerun()


def render_certificates_page():
    """Punto de entrada para la página de certificados"""
    page = CertificatesPage()
    page.render()
