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
            # Tipos de servicios según PROCyMI
            servicios = [
                {"tipo": "Masa", "descripcion": "Calibración de balanzas y sistemas de pesaje"},
                {"tipo": "Temperatura", "descripcion": "Calibración de termómetros y sensores"},
                {"tipo": "Volumen", "descripcion": "Calibración de equipos de medición volumétrica"},
                {"tipo": "Humedad", "descripcion": "Calibración de higrómetros"},
                {"tipo": "Velocidad Angular", "descripcion": "Calibración de centrífugas"}
            ]

            for i, servicio in enumerate(servicios, 1):
                self.certificados.add_certificate({
                    'id': f'EQ{i:03d}',
                    'type': servicio['tipo'],
                    'description': servicio['descripcion'],
                    'status': 'active',
                    'created_at': datetime.now(),
                    'details': {
                        'type': servicio['tipo'],
                        'iso_certified': True,
                        'location': 'Parque Tecnológico Misiones'
                    }
                })
        except Exception as e:
            Logger.error(f"Error agregando datos de ejemplo: {str(e)}")
            raise

    def show_metrics_card(self) -> None:
        """Muestra tarjeta de métricas principales"""
        try:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                total_equipment = len(self.certificados.get_certificates())
                st.metric(
                    "Total Calibraciones",
                    total_equipment,
                    help="Total de equipos calibrados"
                )

            with col2:
                iso_certified = len([
                    c for c in self.certificados.get_certificates()
                    if c.get('details', {}).get('iso_certified', False)
                ])
                st.metric(
                    "Certificaciones ISO",
                    iso_certified,
                    help="Calibraciones con certificación ISO 9001:2015"
                )

            with col3:
                pending = len([
                    c for c in self.certificados.get_certificates()
                    if c['status'] == 'pending'
                ])
                st.metric(
                    "En Proceso",
                    pending,
                    help="Calibraciones en proceso"
                )

            with col4:
                recalibration = len([
                    c for c in self.certificados.get_certificates()
                    if c.get('next_calibration') and
                    (c['next_calibration'] - datetime.now()).days < 30
                ])
                st.metric(
                    "Recalibraciones Próximas",
                    recalibration,
                    help="Equipos que requieren recalibración en 30 días"
                )

        except Exception as e:
            Logger.error(f"Error mostrando métricas: {str(e)}")
            st.error("Error al mostrar métricas")

    def show_requests_timeline(self) -> None:
        """Muestra línea de tiempo de calibraciones"""
        try:
            st.subheader("Historial de Calibraciones")

            # Gráfico de calibraciones por mes
            certificates = self.certificados.get_certificates()
            if not certificates:
                st.info("No hay datos de calibraciones para mostrar")
                return

            # Agregar espacio
            st.markdown("<br>", unsafe_allow_html=True)

            # Gráfico 1: Calibraciones Mensuales
            monthly_data = {}
            for cert in certificates:
                month = cert['created_at'].strftime('%Y-%m')
                monthly_data[month] = monthly_data.get(month, 0) + 1

            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=list(monthly_data.keys()),
                y=list(monthly_data.values()),
                name='Calibraciones por Mes'
            ))
            fig1.update_layout(
                title="Calibraciones Mensuales",
                xaxis_title="Mes",
                yaxis_title="Cantidad",
                height=400,
                width=None,  # Esto permite que ocupe el ancho completo
                showlegend=True
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Agregar espacio entre gráficos
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Gráfico 2: Tipos de Equipos
            equipment_types = {}
            for cert in certificates:
                eq_type = cert.get('details', {}).get('type', 'Otros')
                equipment_types[eq_type] = equipment_types.get(eq_type, 0) + 1

            fig2 = go.Figure(data=[
                go.Pie(
                    labels=list(equipment_types.keys()),
                    values=list(equipment_types.values()),
                    hole=.3
                )
            ])
            fig2.update_layout(
                title="Tipos de Equipos Calibrados",
                height=400,
                width=None,
                showlegend=True
            )
            st.plotly_chart(fig2, use_container_width=True)

        except Exception as e:
            Logger.error(f"Error mostrando línea de tiempo: {str(e)}")
            st.error("Error al mostrar historial de calibraciones")

    def show_provider_stats(self) -> None:
        """Muestra estadísticas de servicios metrológicos"""
        try:
            st.subheader("Análisis de Servicios")

            # Agregar espacio
            st.markdown("<br>", unsafe_allow_html=True)

            # Gráfico 1: Estado de calibraciones
            status_counts = {}
            for cert in self.certificados.get_certificates():
                status = cert.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1

            fig1 = go.Figure(data=[
                go.Bar(
                    name='Estado de Calibraciones',
                    x=list(status_counts.keys()),
                    y=list(status_counts.values()),
                    text=list(status_counts.values()),
                    textposition='auto'
                )
            ])
            fig1.update_layout(
                title="Estado de Calibraciones",
                xaxis_title="Estado",
                yaxis_title="Cantidad",
                height=400,
                width=None,
                showlegend=True
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Agregar espacio entre gráficos
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Gráfico 2: Tiempo promedio de calibración
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

            fig2 = go.Figure(data=[
                go.Bar(
                    name='Tiempo Promedio',
                    x=list(avg_times.keys()),
                    y=list(avg_times.values()),
                    text=[f"{v:.1f} días" for v in avg_times.values()],
                    textposition='auto'
                )
            ])
            fig2.update_layout(
                title="Tiempo Promedio de Calibración por Tipo",
                xaxis_title="Tipo de Equipo",
                yaxis_title="Días",
                height=400,
                width=None,
                showlegend=True
            )
            st.plotly_chart(fig2, use_container_width=True)

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
            # Panel de Control
            st.header("📊 Panel de Control")
            self.show_metrics_card()
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Gestión
            st.header("🛠️ Gestión de Equipos y Calibraciones")
            tab1, tab2 = st.tabs(["📝 ABM Equipos", "🔧 ABM Calibraciones"])
            with tab1:
                self._render_equipment_crud()
            with tab2:
                self._render_calibration_crud()
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Estadísticas
            st.header("📈 Estadísticas y Análisis")

            # Calibraciones Mensuales
            self.show_requests_timeline()
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Análisis de Servicios
            self.show_provider_stats()

        except Exception as e:
            Logger.error(f"Error en dashboard: {str(e)}")
            st.error("Error cargando el dashboard")

    def _render_equipment_crud(self) -> None:
        """Renderiza ABM de equipos"""
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### Alta de Equipos")
            with st.form("new_equipment"):
                eq_id = st.text_input("ID del Equipo")
                eq_type = st.selectbox(
                    "Tipo de Servicio",
                    [
                        "Masa",
                        "Temperatura",
                        "Volumen",
                        "Humedad",
                        "Velocidad Angular"
                    ]
                )
                client = st.text_input("Cliente")
                location = st.selectbox(
                    "Ubicación",
                    [
                        "Parque Tecnológico Misiones",
                        "Universidad Nacional de Misiones",
                        "Laboratorio Móvil"
                    ]
                )
                details = st.text_area("Detalles Técnicos")
                iso_certified = st.checkbox("Requiere Certificación ISO 9001:2015")

                if st.form_submit_button("Registrar Equipo"):
                    try:
                        self.certificados.add_certificate({
                            'id': eq_id,
                            'type': eq_type,
                            'client': client,
                            'location': location,
                            'details': {
                                'description': details,
                                'iso_certified': iso_certified,
                                'service_type': eq_type
                            },
                            'status': 'pending',
                            'created_at': datetime.now()
                        })
                        st.success("✅ Equipo registrado exitosamente")
                    except Exception as e:
                        st.error(f"❌ Error al registrar equipo: {str(e)}")

    def _render_calibration_crud(self) -> None:
        """Renderiza CRUD de calibraciones"""
        # Alta de Calibración
        with st.expander("Nueva Calibración"):
            with st.form("new_calibration"):
                equipment_id = st.selectbox(
                    "Equipo",
                    [eq['id'] for eq in self.certificados.get_certificates()]
                )

                # Tipo de servicio
                service_type = st.selectbox(
                    "Tipo de Servicio",
                    [
                        "Calibración de Balanzas",
                        "Calibración de Termómetros",
                        "Calibración de Material Volumétrico",
                        "Calibración de Higrómetros",
                        "Calibración de Centrífugas",
                        "Verificación de Balanzas",
                        "Mantenimiento Preventivo",
                        "Asesoramiento Técnico"
                    ]
                )

                # Norma aplicable
                standard = st.selectbox(
                    "Norma Aplicable",
                    [
                        "ISO 9001:2015",
                        "ISO/IEC 17025:2017",
                        "OIML R76",
                        "OIML R111"
                    ]
                )

                # Ubicación del servicio
                location = st.selectbox(
                    "Ubicación del Servicio",
                    [
                        "Laboratorio PROCyMI",
                        "Instalaciones del Cliente",
                        "Laboratorio Móvil"
                    ]
                )

                # Fechas
                col1, col2 = st.columns(2)
                with col1:
                    calibration_date = st.date_input("Fecha de Calibración")
                with col2:
                    next_calibration = st.date_input("Próxima Calibración")

                # Detalles técnicos
                technical_details = st.text_area("Detalles Técnicos")

                # Incertidumbre de medición
                uncertainty = st.text_input("Incertidumbre de Medición")

                # Condiciones ambientales
                col1, col2, col3 = st.columns(3)
                with col1:
                    temperature = st.number_input("Temperatura (°C)", value=20.0)
                with col2:
                    humidity = st.number_input("Humedad (%)", value=50.0)
                with col3:
                    pressure = st.number_input("Presión (hPa)", value=1013.25)

                # Trazabilidad
                traceability = st.text_area("Trazabilidad de Patrones")

                # Observaciones
                observations = st.text_area("Observaciones")

                if st.form_submit_button("Registrar Calibración"):
                    try:
                        self.certificados.update_certificate(equipment_id, {
                            'calibration_date': calibration_date,
                            'next_calibration': next_calibration,
                            'status': 'calibrated',
                            'details': {
                                'service_type': service_type,
                                'standard': standard,
                                'location': location,
                                'technical_details': technical_details,
                                'uncertainty': uncertainty,
                                'environmental_conditions': {
                                    'temperature': temperature,
                                    'humidity': humidity,
                                    'pressure': pressure
                                },
                                'traceability': traceability,
                                'observations': observations,
                                'completion_date': datetime.now()
                            }
                        })
                        st.success("✅ Calibración registrada exitosamente")
                    except Exception as e:
                        st.error(f"❌ Error al registrar calibración: {str(e)}")

        # Historial de Calibraciones
        with st.expander("Historial de Calibraciones"):
            calibrated = [
                cert for cert in self.certificados.get_certificates()
                if cert.get('status') == 'calibrated'
            ]
            if calibrated:
                for cert in calibrated:
                    with st.container():
                        col1, col2 = st.columns([2,1])
                        with col1:
                            st.markdown(f"### Equipo: {cert['id']}")
                            st.write(f"Tipo de Servicio: {cert.get('details', {}).get('service_type', 'N/A')}")
                            st.write(f"Norma: {cert.get('details', {}).get('standard', 'N/A')}")
                        with col2:
                            st.write(f"Última calibración: {cert.get('calibration_date', 'N/A')}")
                            st.write(f"Próxima calibración: {cert.get('next_calibration', 'N/A')}")

                        # Detalles técnicos
                        if st.checkbox("Ver detalles técnicos", key=f"details_{cert['id']}"):
                            details = cert.get('details', {})
                            st.write("#### Detalles Técnicos")
                            st.write(f"Incertidumbre: {details.get('uncertainty', 'N/A')}")
                            st.write("Condiciones Ambientales:")
                            env = details.get('environmental_conditions', {})
                            st.write(f"- Temperatura: {env.get('temperature', 'N/A')} °C")
                            st.write(f"- Humedad: {env.get('humidity', 'N/A')} %")
                            st.write(f"- Presión: {env.get('pressure', 'N/A')} hPa")
                            st.write(f"Trazabilidad: {details.get('traceability', 'N/A')}")

                        st.divider()
            else:
                st.info("No hay calibraciones registradas")

    # ... resto del código ...
