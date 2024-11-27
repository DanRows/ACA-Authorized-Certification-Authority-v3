from datetime import datetime
from typing import Dict, List, Optional

import streamlit as st

from app.components.certificados import Certificados
from app.utils.logger import Logger


class CertificatesPage:
    def __init__(self):
        self.certificados = Certificados()

    def render(self) -> None:
        try:
            st.title("Certificados")

            # Mostrar estadísticas
            self._render_stats()

            # Mostrar lista de certificados
            self._render_certificates_list()

        except Exception as e:
            Logger.error(f"Error en página de certificados: {str(e)}")
            st.error("Error al cargar la página de certificados")

    def _render_stats(self) -> None:
        total = self.certificados.get_total()
        st.metric("Total de Certificados", total)

    def _render_certificates_list(self) -> None:
        certificates = self.certificados.get_certificates()

        if not certificates:
            st.info("No hay certificados disponibles")
            return

        for cert in certificates:
            with st.expander(f"Certificado {cert['id']}", expanded=False):
                st.write(f"Fecha: {cert['created_at']}")
                st.write(f"Estado: {cert.get('status', 'N/A')}")
                if cert.get('details'):
                    st.json(cert['details'])
