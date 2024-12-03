from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd
import streamlit as st

from app.components.certificados import Certificados
from app.utils.logger import Logger


class CertificatesPage:
    def __init__(self):
        self.certificados = Certificados()
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Inicializa el estado de la página"""
        if 'editing_certificate' not in st.session_state:
            st.session_state.editing_certificate = None

    def render(self) -> None:
        """Renderiza la página de gestión de certificados"""
        try:
            st.title("Gestión de Certificados de Calibración")

            # Tabs para diferentes secciones
            tab1, tab2, tab3 = st.tabs([
                "📝 Nuevo Certificado",
                "📋 Certificados Activos",
                "📊 Resumen"
            ])

            with tab1:
                self._render_new_certificate_form()
            with tab2:
                self._render_certificates_list()
            with tab3:
                self._render_certificates_summary()

        except Exception as e:
            Logger.error(f"Error en página de certificados: {str(e)}")
            st.error("Error cargando certificados")

    def _render_new_certificate_form(self) -> None:
        """Renderiza formulario de nuevo certificado"""
        with st.form("new_certificate"):
            st.subheader("Nuevo Certificado de Calibración")

            # Información básica
            col1, col2 = st.columns(2)
            with col1:
                client = st.text_input("Cliente")
                equipment_type = st.selectbox(
                    "Tipo de Equipo",
                    [
                        "Balanzas",
                        "Pesas",
                        "Termómetros",
                        "Material Volumétrico",
                        "Higrómetros"
                    ]
                )
                model = st.text_input("Modelo")
            with col2:
                serial = st.text_input("Número de Serie")
                brand = st.text_input("Marca")
                internal_code = st.text_input("Código Interno Cliente")

            # Detalles de calibración
            st.subheader("Detalles de Calibración")
            col1, col2, col3 = st.columns(3)
            with col1:
                calibration_date = st.date_input("Fecha de Calibración")
                location = st.selectbox(
                    "Ubicación",
                    [
                        "Laboratorio PROCyMI",
                        "Instalaciones del Cliente",
                        "Laboratorio Móvil"
                    ]
                )
            with col2:
                next_calibration = st.date_input(
                    "Próxima Calibración",
                    value=datetime.now() + timedelta(days=365)
                )
                standard = st.selectbox(
                    "Norma Aplicable",
                    [
                        "OIML R76",
                        "OIML R111",
                        "ISO/IEC 17025:2017"
                    ]
                )
            with col3:
                measurement_range = st.text_input("Rango de Medición")
                uncertainty = st.text_input("Incertidumbre")

            # Condiciones ambientales
            st.subheader("Condiciones Ambientales")
            col1, col2, col3 = st.columns(3)
            with col1:
                temperature = st.number_input("Temperatura (°C)", value=20.0)
            with col2:
                humidity = st.number_input("Humedad (%)", value=50.0)
            with col3:
                pressure = st.number_input("Presión (hPa)", value=1013.25)

            # Observaciones
            observations = st.text_area("Observaciones")

            if st.form_submit_button("Registrar Certificado"):
                try:
                    self.certificados.add_certificate({
                        'id': f'CERT{len(self.certificados.get_certificates()) + 1:04d}',
                        'client': client,
                        'type': equipment_type,
                        'status': 'active',
                        'created_at': datetime.now(),
                        'details': {
                            'model': model,
                            'serial': serial,
                            'brand': brand,
                            'internal_code': internal_code,
                            'calibration_date': calibration_date,
                            'next_calibration': next_calibration,
                            'location': location,
                            'standard': standard,
                            'measurement_range': measurement_range,
                            'uncertainty': uncertainty,
                            'environmental_conditions': {
                                'temperature': temperature,
                                'humidity': humidity,
                                'pressure': pressure
                            },
                            'observations': observations
                        }
                    })
                    st.success("✅ Certificado registrado exitosamente")
                except Exception as e:
                    st.error(f"❌ Error al registrar certificado: {str(e)}")

    def _render_certificates_list(self) -> None:
        """Renderiza lista de certificados activos"""
        certificates = self.certificados.get_certificates()

        if not certificates:
            st.info("No hay certificados registrados")
            return

        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            client_filter = st.text_input("Buscar por Cliente")
        with col2:
            type_filter = st.multiselect(
                "Tipo de Equipo",
                ["Balanzas", "Pesas", "Termómetros", "Material Volumétrico", "Higrómetros"]
            )
        with col3:
            status_filter = st.multiselect(
                "Estado",
                ["active", "expired", "revoked"]
            )

        # Aplicar filtros
        filtered_certs = certificates
        if client_filter:
            filtered_certs = [
                cert for cert in filtered_certs
                if client_filter.lower() in cert.get('client', '').lower()
            ]
        if type_filter:
            filtered_certs = [
                cert for cert in filtered_certs
                if cert.get('type') in type_filter
            ]
        if status_filter:
            filtered_certs = [
                cert for cert in filtered_certs
                if cert.get('status') in status_filter
            ]

        # Mostrar certificados filtrados
        for cert in filtered_certs:
            with st.expander(
                f"📄 {cert['id']} - {cert.get('client', 'N/A')} ({cert.get('type', 'N/A')})",
                expanded=False
            ):
                col1, col2 = st.columns([3, 1])
                with col1:
                    details = cert.get('details', {})
                    st.write(f"**Equipo:** {cert.get('type')} - {details.get('brand')} {details.get('model')}")
                    st.write(f"**Serie:** {details.get('serial')} | **Código:** {details.get('internal_code')}")
                    st.write(f"**Calibración:** {details.get('calibration_date')} | **Próxima:** {details.get('next_calibration')}")
                    st.write(f"**Norma:** {details.get('standard')} | **Ubicación:** {details.get('location')}")
                with col2:
                    if st.button("🖨️ Imprimir", key=f"print_{cert['id']}"):
                        st.info("Función de impresión en desarrollo")
                    if st.button("📝 Editar", key=f"edit_{cert['id']}"):
                        st.session_state.editing_certificate = cert['id']
                    if st.button("❌ Revocar", key=f"revoke_{cert['id']}"):
                        if self.certificados.update_certificate(cert['id'], {'status': 'revoked'}):
                            st.success("Certificado revocado")
                            st.rerun()

    def _render_certificates_summary(self) -> None:
        """Renderiza resumen de certificados"""
        certificates = self.certificados.get_certificates()

        if not certificates:
            st.info("No hay datos para mostrar")
            return

        # Convertir a DataFrame para análisis
        df = pd.DataFrame(certificates)

        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Certificados", len(certificates))
        with col2:
            active = len([c for c in certificates if c.get('status') == 'active'])
            st.metric("Certificados Activos", active)
        with col3:
            expired = len([
                c for c in certificates
                if c.get('details', {}).get('next_calibration') and
                c.get('details', {}).get('next_calibration') < datetime.now()
            ])
            st.metric("Certificados Vencidos", expired)

        # Gráficos de análisis
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Certificados por Tipo")
            type_counts = df['type'].value_counts()
            st.bar_chart(type_counts)
        with col2:
            st.subheader("Certificados por Ubicación")
            location_counts = df.apply(
                lambda x: x.get('details', {}).get('location', 'N/A'),
                axis=1
            ).value_counts()
            st.bar_chart(location_counts)


def render_certificates_page():
    """Punto de entrada para la página de certificados"""
    try:
        page = CertificatesPage()
        page.render()
    except Exception as e:
        Logger.error(f"Error en página de certificados: {str(e)}")
        st.error("Error cargando la página de certificados")
