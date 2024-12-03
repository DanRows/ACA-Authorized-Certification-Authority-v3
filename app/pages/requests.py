from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import streamlit as st

from app.components.solicitudes import Solicitudes
from app.utils.logger import Logger


class RequestsPage:
    def __init__(self):
        self.solicitudes = Solicitudes()
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Inicializa el estado de la página"""
        if 'editing_request' not in st.session_state:
            st.session_state.editing_request = None

    def render(self) -> None:
        """Renderiza la página de solicitudes"""
        try:
            st.title("Gestión de Solicitudes de Calibración")

            # Tabs para diferentes secciones
            tab1, tab2, tab3 = st.tabs([
                "📝 Nueva Solicitud",
                "📋 Solicitudes Activas",
                "📊 Resumen"
            ])

            with tab1:
                self._render_new_request_form()
            with tab2:
                self._render_requests_list()
            with tab3:
                self._render_requests_summary()

        except Exception as e:
            Logger.error(f"Error en página de solicitudes: {str(e)}")
            st.error("Error cargando solicitudes")

    def _render_new_request_form(self) -> None:
        """Renderiza formulario de nueva solicitud"""
        with st.form("new_request"):
            st.subheader("Nueva Solicitud de Calibración")

            # Información del cliente
            st.markdown("##### Información del Cliente")
            col1, col2 = st.columns(2)
            with col1:
                client = st.text_input("Cliente")
                contact = st.text_input("Persona de Contacto")
            with col2:
                email = st.text_input("Email")
                phone = st.text_input("Teléfono")

            # Información del servicio
            st.markdown("##### Detalles del Servicio")
            col1, col2, col3 = st.columns(3)
            with col1:
                service_type = st.selectbox(
                    "Tipo de Servicio",
                    [
                        "Calibración de Balanzas",
                        "Calibración de Termómetros",
                        "Calibración de Material Volumétrico",
                        "Calibración de Higrómetros",
                        "Verificación de Balanzas",
                        "Mantenimiento Preventivo"
                    ]
                )
            with col2:
                urgency = st.selectbox(
                    "Urgencia",
                    ["Normal", "Urgente", "Muy Urgente"]
                )
            with col3:
                location = st.selectbox(
                    "Ubicación del Servicio",
                    ["Laboratorio PROCyMI", "Instalaciones del Cliente"]
                )

            # Detalles del equipo
            st.markdown("##### Información del Equipo")
            col1, col2 = st.columns(2)
            with col1:
                equipment_type = st.selectbox(
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
                model = st.text_input("Modelo")
            with col2:
                serial = st.text_input("Número de Serie")
                last_calibration = st.date_input(
                    "Última Calibración",
                    value=None,
                    help="Dejar vacío si es primera calibración"
                )

            # Requisitos especiales
            st.markdown("##### Requisitos Especiales")
            col1, col2 = st.columns(2)
            with col1:
                needs_adjustment = st.checkbox("Requiere Ajuste")
                needs_maintenance = st.checkbox("Requiere Mantenimiento")
            with col2:
                iso_required = st.checkbox("Requiere Certificación ISO")
                express_service = st.checkbox("Servicio Express")

            # Observaciones
            observations = st.text_area("Observaciones Adicionales")

            # Fecha deseada
            desired_date = st.date_input(
                "Fecha Deseada",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=7)
            )

            if st.form_submit_button("Enviar Solicitud"):
                self._create_request(
                    client=client,
                    contact=contact,
                    email=email,
                    phone=phone,
                    service_type=service_type,
                    urgency=urgency,
                    location=location,
                    equipment={
                        'type': equipment_type,
                        'brand': brand,
                        'model': model,
                        'serial': serial,
                        'last_calibration': last_calibration
                    },
                    requirements={
                        'needs_adjustment': needs_adjustment,
                        'needs_maintenance': needs_maintenance,
                        'iso_required': iso_required,
                        'express_service': express_service
                    },
                    observations=observations,
                    desired_date=desired_date
                )

    def _render_requests_list(self) -> None:
        """Renderiza lista de solicitudes activas"""
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 Buscar", placeholder="Cliente o ID")
        with col2:
            status_filter = st.multiselect(
                "Estado",
                ["Pendiente", "En Proceso", "Completada", "Cancelada"]
            )
        with col3:
            urgency_filter = st.multiselect(
                "Urgencia",
                ["Normal", "Urgente", "Muy Urgente"]
            )

        # Obtener y filtrar solicitudes
        requests = self.solicitudes.get_requests()
        filtered = self._apply_filters(requests, search, status_filter, urgency_filter)

        if not filtered:
            st.info("No hay solicitudes que coincidan con los filtros")
            return

        # Mostrar solicitudes
        for req in filtered:
            with st.expander(
                f"📋 {req['id']} - {req.get('client', 'N/A')} ({req.get('service_type', 'N/A')})",
                expanded=False
            ):
                self._render_request_details(req)

    def _render_request_details(self, request: Dict) -> None:
        """Renderiza detalles de una solicitud"""
        col1, col2 = st.columns([3, 1])

        with col1:
            # Información básica
            st.markdown(f"""
                **Cliente:** {request.get('client', 'N/A')}
                **Contacto:** {request.get('contact', 'N/A')}
                **Email:** {request.get('email', 'N/A')}
                **Teléfono:** {request.get('phone', 'N/A')}
            """)

            # Detalles del servicio
            st.markdown("##### Detalles del Servicio")
            st.markdown(f"""
                **Tipo:** {request.get('service_type', 'N/A')}
                **Urgencia:** {request.get('urgency', 'N/A')}
                **Ubicación:** {request.get('location', 'N/A')}
                **Fecha Deseada:** {request.get('desired_date', 'N/A')}
            """)

            # Información del equipo
            if equipment := request.get('equipment', {}):
                st.markdown("##### Equipo")
                st.markdown(f"""
                    **Tipo:** {equipment.get('type', 'N/A')}
                    **Marca:** {equipment.get('brand', 'N/A')}
                    **Modelo:** {equipment.get('model', 'N/A')}
                    **Serie:** {equipment.get('serial', 'N/A')}
                """)

        with col2:
            # Acciones
            st.markdown("##### Acciones")
            status = request.get('status', 'pending')

            if status == 'pending':
                if st.button("✅ Aprobar", key=f"approve_{request['id']}"):
                    self._approve_request(request)
                if st.button("❌ Rechazar", key=f"reject_{request['id']}"):
                    self._reject_request(request)
            elif status == 'approved':
                if st.button("🔄 Iniciar", key=f"start_{request['id']}"):
                    self._start_request(request)
            elif status == 'in_progress':
                if st.button("✨ Completar", key=f"complete_{request['id']}"):
                    self._complete_request(request)

            if st.button("📝 Editar", key=f"edit_{request['id']}"):
                st.session_state.editing_request = request['id']

    def _render_requests_summary(self) -> None:
        """Renderiza resumen de solicitudes"""
        requests = self.solicitudes.get_requests()
        if not requests:
            st.info("No hay datos para analizar")
            return

        # Convertir a DataFrame
        df = pd.DataFrame(requests)

        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Solicitudes", len(df))
        with col2:
            pending = len(df[df['status'] == 'pending'])
            st.metric("Pendientes", pending)
        with col3:
            in_progress = len(df[df['status'] == 'in_progress'])
            st.metric("En Proceso", in_progress)
        with col4:
            completed = len(df[df['status'] == 'completed'])
            st.metric("Completadas", completed)

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            # Distribución por estado
            fig = px.pie(
                df,
                names='status',
                title="Distribución por Estado"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Solicitudes por tipo de servicio
            service_counts = df['service_type'].value_counts()
            fig = px.bar(
                service_counts,
                title="Solicitudes por Tipo de Servicio"
            )
            st.plotly_chart(fig, use_container_width=True)

    def _create_request(self, **kwargs) -> None:
        """Crea una nueva solicitud"""
        try:
            request = {
                'id': f'REQ{len(self.solicitudes.get_requests()) + 1:04d}',
                'status': 'pending',
                'created_at': datetime.now(),
                **kwargs
            }
            self.solicitudes.add_request(request)
            st.success("✅ Solicitud enviada exitosamente")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Error al enviar solicitud: {str(e)}")

    def _apply_filters(self, requests: List[Dict], search: str,
                      status_filter: List[str], urgency_filter: List[str]) -> List[Dict]:
        """Aplica filtros a la lista de solicitudes"""
        filtered = requests

        if search:
            filtered = [
                r for r in filtered
                if search.lower() in r.get('client', '').lower() or
                search.lower() in r.get('id', '').lower()
            ]

        if status_filter:
            filtered = [
                r for r in filtered
                if r.get('status', '').title() in status_filter
            ]

        if urgency_filter:
            filtered = [
                r for r in filtered
                if r.get('urgency', '') in urgency_filter
            ]

        return filtered

    def _approve_request(self, request: Dict) -> None:
        """Aprueba una solicitud"""
        try:
            request['status'] = 'approved'
            self.solicitudes.update_request(request['id'], request)
            st.success("✅ Solicitud aprobada")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error al aprobar solicitud: {str(e)}")

    def _reject_request(self, request: Dict) -> None:
        """Rechaza una solicitud"""
        try:
            request['status'] = 'rejected'
            self.solicitudes.update_request(request['id'], request)
            st.success("Solicitud rechazada")
            st.rerun()
        except Exception as e:
            st.error(f"Error al rechazar solicitud: {str(e)}")

    def _start_request(self, request: Dict) -> None:
        """Inicia el proceso de una solicitud"""
        try:
            request['status'] = 'in_progress'
            request['started_at'] = datetime.now()
            self.solicitudes.update_request(request['id'], request)
            st.success("✅ Proceso iniciado")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error al iniciar proceso: {str(e)}")

    def _complete_request(self, request: Dict) -> None:
        """Completa una solicitud"""
        try:
            request['status'] = 'completed'
            request['completed_at'] = datetime.now()
            self.solicitudes.update_request(request['id'], request)
            st.success("✅ Solicitud completada")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error al completar solicitud: {str(e)}")


def render_requests_page():
    """Punto de entrada para la página de solicitudes"""
    try:
        page = RequestsPage()
        page.render()
    except Exception as e:
        Logger.error(f"Error en página de solicitudes: {str(e)}")
        st.error("Error cargando la página de solicitudes")
