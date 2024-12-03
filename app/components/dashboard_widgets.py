from datetime import datetime
from typing import Dict, List

import plotly.graph_objects as go  # type: ignore
import streamlit as st  # type: ignore

from app.components.analytics_dashboard import AnalyticsDashboard
from app.components.certificados import Certificados
from app.components.solicitudes import Solicitudes
from app.utils.db import DatabaseManager
from app.utils.logger import Logger


class DashboardWidgets:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, solicitudes: Solicitudes, certificados: Certificados):
        if not self._initialized:
            try:
                self.solicitudes = solicitudes
                self.certificados = certificados
                # Agregar datos de ejemplo solo una vez
                if len(self.solicitudes.get_requests()) == 0:
                    self._add_sample_data()
                self.__class__._initialized = True
            except Exception as e:
                Logger.error(f"Error inicializando DashboardWidgets: {str(e)}")
                raise

    def _add_sample_data(self) -> None:
        """Agrega datos de ejemplo para desarrollo"""
        try:
            # Agregar algunas solicitudes de ejemplo
            self.solicitudes.add_request({
                'id': '001',
                'status': 'pending',
                'provider': 'openai',
                'created_at': datetime.now()
            })
            self.solicitudes.add_request({
                'id': '002',
                'status': 'completed',
                'provider': 'vertex',
                'created_at': datetime.now()
            })

            # Agregar algunos certificados de ejemplo
            self.certificados.add_certificate({
                'id': '001',
                'status': 'active',
                'created_at': datetime.now(),
                'details': {'type': 'basic'}
            })
            self.certificados.add_certificate({
                'id': '002',
                'status': 'pending',
                'created_at': datetime.now(),
                'details': {'type': 'advanced'}
            })
        except Exception as e:
            Logger.warning(f"No se pudieron agregar datos de ejemplo: {str(e)}")

    def show_metrics_card(self) -> None:
        """Muestra tarjeta de métricas principales"""
        try:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                total_equipment = len(self.certificados.get_certificates())
                st.metric(
                    "Equipos Calibrados",
                    total_equipment,
                    help="Total de equipos calibrados"
                )

            with col2:
                pending_calibrations = len([
                    c for c in self.certificados.get_certificates()
                    if c['status'] == 'pending'
                ])
                st.metric(
                    "Calibraciones Pendientes",
                    pending_calibrations,
                    help="Calibraciones en proceso"
                )

            with col3:
                success_rate = self._calculate_success_rate()
                st.metric(
                    "Satisfacción Cliente",
                    f"{success_rate}%",
                    help="Índice de satisfacción del cliente"
                )

            with col4:
                # Calcular equipos que necesitan recalibración pronto
                due_soon = len([
                    c for c in self.certificados.get_certificates()
                    if c.get('next_calibration') and
                    (c['next_calibration'] - datetime.now()).days < 30
                ])
                st.metric(
                    "Próximas Calibraciones",
                    due_soon,
                    help="Equipos que requieren calibración en los próximos 30 días"
                )

        except Exception as e:
            Logger.error(f"Error mostrando métricas: {str(e)}")
            st.error("Error al mostrar métricas")

    def show_requests_timeline(self) -> None:
        """Muestra línea de tiempo de calibraciones"""
        try:
            st.subheader("Historial de Calibraciones")

            # Crear dos columnas
            col1, col2 = st.columns(2)

            with col1:
                # Gráfico de calibraciones por mes
                certificates = self.certificados.get_certificates()
                if not certificates:
                    st.info("No hay datos de calibraciones para mostrar")
                    return

                # Agrupar por mes
                monthly_data = {}
                for cert in certificates:
                    month = cert['created_at'].strftime('%Y-%m')
                    monthly_data[month] = monthly_data.get(month, 0) + 1

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=list(monthly_data.keys()),
                    y=list(monthly_data.values()),
                    name='Calibraciones por Mes'
                ))
                fig.update_layout(
                    title="Calibraciones Mensuales",
                    xaxis_title="Mes",
                    yaxis_title="Cantidad",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Gráfico de tipos de equipos calibrados
                equipment_types = {}
                for cert in certificates:
                    eq_type = cert.get('details', {}).get('type', 'Otros')
                    equipment_types[eq_type] = equipment_types.get(eq_type, 0) + 1

                fig = go.Figure(data=[
                    go.Pie(
                        labels=list(equipment_types.keys()),
                        values=list(equipment_types.values()),
                        hole=.3
                    )
                ])
                fig.update_layout(
                    title="Tipos de Equipos Calibrados",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            Logger.error(f"Error mostrando línea de tiempo: {str(e)}")
            st.error("Error al mostrar historial de calibraciones")

    def show_provider_stats(self) -> None:
        """Muestra estadísticas de servicios metrológicos"""
        try:
            st.subheader("Análisis de Servicios")

            # Crear dos columnas
            col1, col2 = st.columns(2)

            with col1:
                # Estado de calibraciones
                status_counts = {}
                for cert in self.certificados.get_certificates():
                    status = cert.get('status', 'unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1

                fig = go.Figure(data=[
                    go.Bar(
                        name='Estado de Calibraciones',
                        x=list(status_counts.keys()),
                        y=list(status_counts.values()),
                        text=list(status_counts.values()),
                        textposition='auto'
                    )
                ])
                fig.update_layout(
                    title="Estado de Calibraciones",
                    xaxis_title="Estado",
                    yaxis_title="Cantidad",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Tiempo promedio de calibración por tipo de equipo
                equipment_times = {}
                for cert in self.certificados.get_certificates():
                    if cert.get('created_at') and cert.get('details', {}).get('completion_date'):
                        eq_type = cert.get('details', {}).get('type', 'Otros')
                        time_diff = (cert['details']['completion_date'] - cert['created_at']).days
                        if eq_type not in equipment_times:
                            equipment_times[eq_type] = []
                        equipment_times[eq_type].append(time_diff)

                avg_times = {
                    k: sum(v)/len(v)
                    for k, v in equipment_times.items()
                }

                fig = go.Figure(data=[
                    go.Bar(
                        name='Tiempo Promedio',
                        x=list(avg_times.keys()),
                        y=list(avg_times.values()),
                        text=[f"{v:.1f} días" for v in avg_times.values()],
                        textposition='auto'
                    )
                ])
                fig.update_layout(
                    title="Tiempo Promedio de Calibración por Tipo",
                    xaxis_title="Tipo de Equipo",
                    yaxis_title="Días",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            Logger.error(f"Error mostrando estadísticas: {str(e)}")
            st.error("Error al mostrar análisis de servicios")

    def _calculate_success_rate(self) -> float:
        """Calcula la tasa de éxito de las solicitudes"""
        try:
            requests = self.solicitudes.get_requests()
            if not requests:
                return 0.0
            completed = len([r for r in requests if r['status'] == 'completed'])
            return round((completed / len(requests)) * 100, 2)
        except Exception as e:
            Logger.error(f"Error calculando tasa de éxito: {str(e)}")
            return 0.0

    def _render_original_metrics(self) -> None:
        """Renderiza las métricas originales"""
        try:
            col1, col2, col3 = st.columns(3)

            with col1:
                total_requests = len(self.solicitudes.get_requests())
                st.metric("Total Solicitudes", total_requests)

            with col2:
                pending_requests = len([r for r in self.solicitudes.get_requests()
                                    if r['status'] == 'pending'])
                st.metric("Solicitudes Pendientes", pending_requests)

            with col3:
                success_rate = self._calculate_success_rate()
                st.metric("Tasa de Éxito", f"{success_rate}%")
        except Exception as e:
            Logger.error(f"Error mostrando métricas originales: {str(e)}")
            st.error("Error al mostrar métricas originales")

    def render(self) -> None:
        """Renderiza el dashboard"""
        try:
            # Agregar espacio superior
            st.markdown("<br>", unsafe_allow_html=True)

            # Métricas principales
            self.show_metrics_card()

            # Agregar espacio entre secciones
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Operaciones CRUD
            self.show_crud_operations()

            # Agregar espacio entre secciones
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Historial de Calibraciones
            self.show_requests_timeline()

            # Agregar espacio entre secciones
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Análisis de Servicios
            self.show_provider_stats()

        except Exception as e:
            Logger.error(f"Error en dashboard: {str(e)}")
            st.error("Error cargando el dashboard")

    def show_crud_operations(self) -> None:
        """Muestra operaciones CRUD para equipos y calibraciones"""
        try:
            st.subheader("Gestión de Equipos y Calibraciones")

            # Tabs para separar operaciones
            tab1, tab2 = st.tabs(["Equipos", "Calibraciones"])

            with tab1:
                self._render_equipment_crud()

            with tab2:
                self._render_calibration_crud()

        except Exception as e:
            Logger.error(f"Error en operaciones CRUD: {str(e)}")
            st.error("Error en operaciones de gestión")

    def _render_equipment_crud(self) -> None:
        """Renderiza CRUD de equipos"""
        # Alta (Create)
        with st.expander("Agregar Nuevo Equipo"):
            with st.form("new_equipment"):
                eq_id = st.text_input("ID del Equipo")
                eq_type = st.selectbox(
                    "Tipo de Equipo",
                    ["Balanza", "Termómetro", "Manómetro", "Calibrador", "Otro"]
                )
                client = st.text_input("Cliente")
                details = st.text_area("Detalles")

                if st.form_submit_button("Agregar"):
                    try:
                        self.certificados.add_certificate({
                            'id': eq_id,
                            'type': eq_type,
                            'client': client,
                            'details': {'description': details},
                            'status': 'pending',
                            'created_at': datetime.now()
                        })
                        st.success("Equipo agregado exitosamente")
                    except Exception as e:
                        st.error(f"Error al agregar equipo: {str(e)}")

        # Consulta y Modificación (Read & Update)
        with st.expander("Consultar/Modificar Equipos"):
            equipment = self.certificados.get_certificates()
            if equipment:
                for eq in equipment:
                    col1, col2, col3 = st.columns([2,1,1])
                    with col1:
                        st.write(f"ID: {eq['id']} - {eq.get('type', 'N/A')}")
                    with col2:
                        if st.button("Editar", key=f"edit_{eq['id']}"):
                            st.session_state.editing_equipment = eq['id']
                    with col3:
                        if st.button("Eliminar", key=f"delete_{eq['id']}"):
                            if self.certificados.delete_certificate(eq['id']):
                                st.success("Equipo eliminado")
                                st.rerun()

                    # Formulario de edición
                    if st.session_state.get('editing_equipment') == eq['id']:
                        with st.form(f"edit_equipment_{eq['id']}"):
                            new_type = st.selectbox(
                                "Tipo de Equipo",
                                ["Balanza", "Termómetro", "Manómetro", "Calibrador", "Otro"],
                                index=["Balanza", "Termómetro", "Manómetro", "Calibrador", "Otro"].index(eq.get('type', 'Otro'))
                            )
                            new_status = st.selectbox(
                                "Estado",
                                ["pending", "active", "calibrated"],
                                index=["pending", "active", "calibrated"].index(eq.get('status', 'pending'))
                            )

                            if st.form_submit_button("Guardar Cambios"):
                                if self.certificados.update_certificate(eq['id'], {
                                    'type': new_type,
                                    'status': new_status
                                }):
                                    st.success("Cambios guardados")
                                    st.session_state.editing_equipment = None
                                    st.rerun()
            else:
                st.info("No hay equipos registrados")

    def _render_calibration_crud(self) -> None:
        """Renderiza CRUD de calibraciones"""
        # Alta de Calibración
        with st.expander("Nueva Calibración"):
            with st.form("new_calibration"):
                equipment_id = st.selectbox(
                    "Equipo",
                    [eq['id'] for eq in self.certificados.get_certificates()]
                )
                calibration_date = st.date_input("Fecha de Calibración")
                next_calibration = st.date_input("Próxima Calibración")
                observations = st.text_area("Observaciones")

                if st.form_submit_button("Registrar Calibración"):
                    try:
                        self.certificados.update_certificate(equipment_id, {
                            'calibration_date': calibration_date,
                            'next_calibration': next_calibration,
                            'status': 'calibrated',
                            'details': {
                                'observations': observations,
                                'completion_date': datetime.now()
                            }
                        })
                        st.success("Calibración registrada")
                    except Exception as e:
                        st.error(f"Error al registrar calibración: {str(e)}")

        # Historial de Calibraciones
        with st.expander("Historial de Calibraciones"):
            calibrated = [
                cert for cert in self.certificados.get_certificates()
                if cert.get('status') == 'calibrated'
            ]
            if calibrated:
                for cert in calibrated:
                    st.write(f"Equipo: {cert['id']}")
                    st.write(f"Última calibración: {cert.get('calibration_date', 'N/A')}")
                    st.write(f"Próxima calibración: {cert.get('next_calibration', 'N/A')}")
                    st.divider()
            else:
                st.info("No hay calibraciones registradas")

    # ... resto del código ...
