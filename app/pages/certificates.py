from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
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
        if 'certificate_view' not in st.session_state:
            st.session_state.certificate_view = "list"

    def render(self) -> None:
        """Renderiza la página de certificados"""
        try:
            st.title("Gestión de Certificados de Calibración")

            # Menú de navegación
            menu = ["📋 Lista", "➕ Nuevo", "📊 Estadísticas", "🔍 Búsqueda Avanzada"]
            selected = st.radio("", menu, horizontal=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if "Lista" in selected:
                self._render_certificates_list()
            elif "Nuevo" in selected:
                self._render_new_certificate()
            elif "Estadísticas" in selected:
                self._render_statistics()
            else:
                self._render_advanced_search()

        except Exception as e:
            Logger.error(f"Error en página de certificados: {str(e)}")
            st.error("Error cargando certificados")

    def _render_certificates_list(self) -> None:
        """Renderiza lista de certificados"""
        # Filtros rápidos
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 Buscar", placeholder="Cliente o ID")
        with col2:
            status_filter = st.multiselect(
                "Estado",
                ["Activo", "Vencido", "Próximo a vencer"]
            )
        with col3:
            date_range = st.date_input(
                "Rango de fechas",
                value=[datetime.now() - timedelta(days=30), datetime.now()]
            )

        # Obtener y filtrar certificados
        certificates = self.certificados.get_certificates()
        filtered_certs = self._apply_filters(certificates, search, status_filter, date_range)

        if not filtered_certs:
            st.info("No se encontraron certificados con los filtros aplicados")
            return

        # Mostrar certificados
        for cert in filtered_certs:
            with st.expander(f"📄 Certificado {cert['id']} - {cert.get('client', 'N/A')}", expanded=False):
                self._render_certificate_details(cert)

    def _render_certificate_details(self, cert: Dict) -> None:
        """Renderiza detalles de un certificado"""
        col1, col2 = st.columns([3, 1])

        with col1:
            # Información básica
            st.markdown(f"""
                **Cliente:** {cert.get('client', 'N/A')}
                **Equipo:** {cert.get('type', 'N/A')}
                **Fecha de Calibración:** {cert.get('calibration_date', 'N/A')}
                **Próxima Calibración:** {cert.get('next_calibration', 'N/A')}
                **Estado:** {cert.get('status', 'N/A')}
            """)

            # Detalles técnicos
            if details := cert.get('details', {}):
                st.markdown("##### Detalles Técnicos")
                st.markdown(f"""
                    **Modelo:** {details.get('model', 'N/A')}
                    **Serie:** {details.get('serial', 'N/A')}
                    **Rango:** {details.get('measurement_range', 'N/A')}
                    **Incertidumbre:** {details.get('uncertainty', 'N/A')}
                """)

                # Condiciones ambientales
                if env := details.get('environmental_conditions', {}):
                    st.markdown("##### Condiciones Ambientales")
                    st.markdown(f"""
                        **Temperatura:** {env.get('temperature', 'N/A')} °C
                        **Humedad:** {env.get('humidity', 'N/A')} %
                        **Presión:** {env.get('pressure', 'N/A')} hPa
                    """)

        with col2:
            # Acciones
            st.markdown("##### Acciones")
            if st.button("🖨️ Imprimir", key=f"print_{cert['id']}"):
                self._generate_certificate_pdf(cert)
            if st.button("📝 Editar", key=f"edit_{cert['id']}"):
                st.session_state.editing_certificate = cert['id']
            if st.button("🔄 Renovar", key=f"renew_{cert['id']}"):
                self._renew_certificate(cert)
            if st.button("❌ Revocar", key=f"revoke_{cert['id']}"):
                self._revoke_certificate(cert)

    def _render_new_certificate(self) -> None:
        """Renderiza formulario de nuevo certificado"""
        with st.form("new_certificate"):
            st.subheader("Nuevo Certificado de Calibración")

            # Información del cliente
            st.markdown("##### Información del Cliente")
            col1, col2 = st.columns(2)
            with col1:
                client = st.text_input("Cliente")
                contact = st.text_input("Contacto")
            with col2:
                email = st.text_input("Email")
                phone = st.text_input("Teléfono")

            # Información del equipo
            st.markdown("##### Información del Equipo")
            col1, col2, col3 = st.columns(3)
            with col1:
                eq_type = st.selectbox(
                    "Tipo de Equipo",
                    [
                        "Balanza Analítica",
                        "Balanza de Precisión",
                        "Termómetro Digital",
                        "Termómetro Analógico",
                        "Material Volumétrico",
                        "Higrómetro"
                    ]
                )
                brand = st.text_input("Marca")
            with col2:
                model = st.text_input("Modelo")
                serial = st.text_input("Número de Serie")
            with col3:
                measurement_range = st.text_input("Rango de Medición")
                resolution = st.text_input("Resolución")

            # Detalles de calibración
            st.markdown("##### Detalles de Calibración")
            col1, col2 = st.columns(2)
            with col1:
                calibration_date = st.date_input("Fecha de Calibración")
                location = st.selectbox(
                    "Ubicación",
                    ["Laboratorio PROCyMI", "Instalaciones del Cliente"]
                )
            with col2:
                next_calibration = st.date_input(
                    "Próxima Calibración",
                    value=datetime.now() + timedelta(days=365)
                )
                standard = st.selectbox(
                    "Norma Aplicable",
                    ["OIML R76", "OIML R111", "ISO/IEC 17025:2017"]
                )

            # Condiciones ambientales
            st.markdown("##### Condiciones Ambientales")
            col1, col2, col3 = st.columns(3)
            with col1:
                temperature = st.number_input("Temperatura (°C)", value=20.0)
            with col2:
                humidity = st.number_input("Humedad (%)", value=50.0)
            with col3:
                pressure = st.number_input("Presión (hPa)", value=1013.25)

            # Observaciones
            observations = st.text_area("Observaciones")

            if st.form_submit_button("Generar Certificado"):
                self._create_certificate(
                    client, eq_type, calibration_date, next_calibration,
                    {
                        'contact': contact,
                        'email': email,
                        'phone': phone,
                        'brand': brand,
                        'model': model,
                        'serial': serial,
                        'measurement_range': measurement_range,
                        'resolution': resolution,
                        'location': location,
                        'standard': standard,
                        'environmental_conditions': {
                            'temperature': temperature,
                            'humidity': humidity,
                            'pressure': pressure
                        },
                        'observations': observations
                    }
                )

    def _render_statistics(self) -> None:
        """Renderiza estadísticas de certificados"""
        certificates = self.certificados.get_certificates()
        if not certificates:
            st.info("No hay datos para analizar")
            return

        # Convertir a DataFrame
        df = pd.DataFrame(certificates)

        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Certificados", len(df))
        with col2:
            active = len(df[df['status'] == 'active'])
            st.metric("Certificados Activos", active)
        with col3:
            expired = len([
                c for c in certificates
                if c.get('next_calibration') and
                c.get('next_calibration') < datetime.now()
            ])
            st.metric("Certificados Vencidos", expired)
        with col4:
            due_soon = len([
                c for c in certificates
                if c.get('next_calibration') and
                timedelta(0) <= (c['next_calibration'] - datetime.now()) <= timedelta(days=30)
            ])
            st.metric("Próximos a Vencer", due_soon)

        # Gráficos
        col1, col2 = st.columns(2)
        with col1:
            self._render_equipment_distribution(df)
        with col2:
            self._render_calibration_timeline(df)

    def _render_advanced_search(self) -> None:
        """Renderiza búsqueda avanzada"""
        st.subheader("Búsqueda Avanzada de Certificados")

        # Criterios de búsqueda
        with st.expander("🔍 Criterios de Búsqueda", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                client_search = st.text_input("Cliente")
                equipment_type = st.multiselect(
                    "Tipo de Equipo",
                    ["Balanza", "Termómetro", "Material Volumétrico", "Higrómetro"]
                )
                status = st.multiselect(
                    "Estado",
                    ["active", "expired", "revoked"]
                )
            with col2:
                date_range = st.date_input(
                    "Rango de Fechas",
                    value=[datetime.now() - timedelta(days=30), datetime.now()]
                )
                location = st.multiselect(
                    "Ubicación",
                    ["Laboratorio PROCyMI", "Instalaciones del Cliente"]
                )

        # Botón de búsqueda
        if st.button("🔍 Buscar"):
            results = self._search_certificates(
                client_search, equipment_type, status,
                date_range, location
            )
            if results:
                st.success(f"Se encontraron {len(results)} certificados")
                self._display_search_results(results)
            else:
                st.info("No se encontraron certificados con los criterios especificados")

    def _create_certificate(self, client: str, eq_type: str,
                          calibration_date: datetime, next_calibration: datetime,
                          details: Dict) -> None:
        """Crea un nuevo certificado"""
        try:
            certificate = {
                'id': f'CERT{len(self.certificados.get_certificates()) + 1:04d}',
                'client': client,
                'type': eq_type,
                'calibration_date': calibration_date,
                'next_calibration': next_calibration,
                'status': 'active',
                'created_at': datetime.now(),
                'details': details
            }
            self.certificados.add_certificate(certificate)
            st.success("✅ Certificado generado exitosamente")
            st.session_state.certificate_view = "list"
        except Exception as e:
            st.error(f"❌ Error al generar certificado: {str(e)}")

    def _apply_filters(self, certificates: List[Dict], search: str,
                      status_filter: List[str], date_range: List[datetime]) -> List[Dict]:
        """Aplica filtros a la lista de certificados"""
        filtered = certificates

        if search:
            filtered = [
                c for c in filtered
                if search.lower() in c.get('client', '').lower() or
                search.lower() in c.get('id', '').lower()
            ]

        if status_filter:
            filtered = [
                c for c in filtered
                if any(status.lower() in c.get('status', '').lower()
                      for status in status_filter)
            ]

        if date_range and len(date_range) == 2:
            filtered = [
                c for c in filtered
                if date_range[0] <= c.get('calibration_date', datetime.now()) <= date_range[1]
            ]

        return filtered

    def _generate_certificate_pdf(self, cert: Dict) -> None:
        """Genera PDF del certificado"""
        # TODO: Implementar generación de PDF
        st.info("Función de generación de PDF en desarrollo")

    def _renew_certificate(self, cert: Dict) -> None:
        """Renueva un certificado"""
        try:
            new_cert = cert.copy()
            new_cert.update({
                'id': f'CERT{len(self.certificados.get_certificates()) + 1:04d}',
                'calibration_date': datetime.now(),
                'next_calibration': datetime.now() + timedelta(days=365),
                'created_at': datetime.now(),
                'status': 'active'
            })
            self.certificados.add_certificate(new_cert)
            st.success("✅ Certificado renovado exitosamente")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error al renovar certificado: {str(e)}")

    def _revoke_certificate(self, cert: Dict) -> None:
        """Revoca un certificado"""
        try:
            cert['status'] = 'revoked'
            self.certificados.update_certificate(cert['id'], cert)
            st.success("Certificado revocado exitosamente")
            st.rerun()
        except Exception as e:
            st.error(f"Error al revocar certificado: {str(e)}")


def render_certificates_page():
    """Punto de entrada para la página de certificados"""
    try:
        page = CertificatesPage()
        page.render()
    except Exception as e:
        Logger.error(f"Error en página de certificados: {str(e)}")
        st.error("Error cargando la página de certificados")
