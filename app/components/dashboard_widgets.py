from datetime import datetime
from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.components.certificados import Certificados
from app.components.solicitudes import Solicitudes
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
            # Servicios según PROCyMI
            servicios = [
                {
                    "tipo": "Balanzas",
                    "descripcion": "Calibración de balanzas analíticas y de precisión",
                    "norma": "OIML R76",
                    "rango": "Hasta 1000kg"
                },
                {
                    "tipo": "Pesas",
                    "descripcion": "Calibración de pesas patrón",
                    "norma": "OIML R111",
                    "rango": "1mg a 20kg"
                },
                {
                    "tipo": "Termómetros",
                    "descripcion": "Calibración de termómetros digitales y analógicos",
                    "norma": "ISO/IEC 17025:2017",
                    "rango": "-30°C a 200°C"
                },
                {
                    "tipo": "Material Volumétrico",
                    "descripcion": "Calibración de material volumétrico",
                    "norma": "ISO/IEC 17025:2017",
                    "rango": "0.1mL a 2000mL"
                },
                {
                    "tipo": "Higrómetros",
                    "descripcion": "Calibración de higrómetros",
                    "norma": "ISO/IEC 17025:2017",
                    "rango": "10% a 98% HR"
                }
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
                        'rango_medicion': servicio['rango'],
                        'norma': servicio['norma'],
                        'iso_certified': True,
                        'location': 'Laboratorio PROCyMI'
                    }
                })
        except Exception as e:
            Logger.error(f"Error agregando datos de ejemplo: {str(e)}")
            raise

    def show_metrics_card(self) -> None:
        """Muestra tarjeta de métricas principales"""
        try:
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                total_equipment = len(self.certificados.get_certificates())
                st.metric(
                    "Total Calibraciones",
                    total_equipment,
                    help="Total de equipos calibrados"
                )

            with col2:
                oiml_certified = len([
                    c for c in self.certificados.get_certificates()
                    if "OIML" in c.get('details', {}).get('norma', '')
                ])
                st.metric(
                    "Cert. OIML",
                    oiml_certified,
                    help="Calibraciones bajo normas OIML"
                )

            with col3:
                iso_certified = len([
                    c for c in self.certificados.get_certificates()
                    if "17025" in c.get('details', {}).get('norma', '')
                ])
                st.metric(
                    "ISO 17025",
                    iso_certified,
                    help="Calibraciones bajo ISO/IEC 17025:2017"
                )

            with col4:
                onsite = len([
                    c for c in self.certificados.get_certificates()
                    if c.get('details', {}).get('location') == 'Instalaciones del Cliente'
                ])
                st.metric(
                    "In Situ",
                    onsite,
                    help="Calibraciones realizadas en instalaciones del cliente"
                )

            with col5:
                recalibration = len([
                    c for c in self.certificados.get_certificates()
                    if c.get('next_calibration') and
                    (c['next_calibration'] - datetime.now()).days < 30
                ])
                st.metric(
                    "Próximas",
                    recalibration,
                    help="Calibraciones programadas próximos 30 días"
                )

        except Exception as e:
            Logger.error(f"Error mostrando métricas: {str(e)}")
            st.error("Error al mostrar métricas")

    def show_requests_timeline(self) -> None:
        """Muestra línea de tiempo de calibraciones"""
        try:
            st.subheader("Historial de Calibraciones")

            # Filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                tipo_filtro = st.multiselect(
                    "Tipo de Equipo",
                    ["Balanzas", "Pesas", "Termómetros", "Material Volumétrico", "Higrómetros"]
                )
            with col2:
                cliente_filtro = st.text_input("Buscar por Cliente")
            with col3:
                estado_filtro = st.multiselect(
                    "Estado",
                    ["Pendiente", "En Proceso", "Completado", "Vencido"]
                )

            # Aplicar filtros y mostrar datos
            self._show_filtered_timeline(tipo_filtro, cliente_filtro, estado_filtro)

        except Exception as e:
            Logger.error(f"Error mostrando línea de tiempo: {str(e)}")
            st.error("Error al mostrar historial de calibraciones")

    def _show_filtered_timeline(self, tipo_filtro: List[str], cliente_filtro: str, estado_filtro: List[str]) -> None:
        """Muestra la línea de tiempo filtrada"""
        try:
            certificates = self.certificados.get_certificates()

            # Aplicar filtros
            filtered_certs = certificates
            if tipo_filtro:
                filtered_certs = [
                    cert for cert in filtered_certs
                    if cert.get('type') in tipo_filtro
                ]
            if cliente_filtro:
                filtered_certs = [
                    cert for cert in filtered_certs
                    if cliente_filtro.lower() in cert.get('client', '').lower()
                ]
            if estado_filtro:
                filtered_certs = [
                    cert for cert in filtered_certs
                    if cert.get('status') in estado_filtro
                ]

            if not filtered_certs:
                st.info("No hay datos que coincidan con los filtros seleccionados")
                return

            # Crear gráfico de línea de tiempo
            dates = [cert.get('created_at', datetime.now()) for cert in filtered_certs]
            types = [cert.get('type', 'N/A') for cert in filtered_certs]

            fig = go.Figure()

            # Agregar línea de tiempo
            fig.add_trace(go.Scatter(
                x=dates,
                y=types,
                mode='markers',
                name='Calibraciones',
                marker=dict(
                    size=12,
                    symbol='circle'
                )
            ))

            # Configurar layout
            fig.update_layout(
                title="Línea de Tiempo de Calibraciones",
                xaxis_title="Fecha",
                yaxis_title="Tipo de Equipo",
                height=400,
                showlegend=True
            )

            # Mostrar gráfico
            st.plotly_chart(fig, use_container_width=True)

            # Mostrar tabla de detalles
            if st.checkbox("Ver detalles de calibraciones"):
                df = pd.DataFrame(filtered_certs)
                st.dataframe(
                    df,
                    column_config={
                        "created_at": st.column_config.DatetimeColumn("Fecha"),
                        "type": "Tipo",
                        "client": "Cliente",
                        "status": "Estado"
                    },
                    hide_index=True
                )

        except Exception as e:
            Logger.error(f"Error mostrando timeline filtrado: {str(e)}")
            st.error("Error al mostrar línea de tiempo")
