import io
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
import plotly.express as px
import streamlit as st

from app.components.certificados import Certificados
from app.components.metrics_dashboard import MetricsDashboard
from app.components.solicitudes import Solicitudes
from app.utils.cache import CacheManager
from app.utils.logger import Logger


class ReportGenerator:
    def __init__(self):
        self.metrics = MetricsDashboard()
        self.solicitudes = Solicitudes()
        self.certificados = Certificados()
        self.cache_manager = CacheManager()
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Inicializa el estado del generador de reportes"""
        if 'report_data' not in st.session_state:
            st.session_state.report_data = None
        if 'last_report_type' not in st.session_state:
            st.session_state.last_report_type = None

    def _get_report_data(self, report_type: str, date_range: Tuple[datetime, datetime]) -> pd.DataFrame:
        """Obtiene datos del reporte con caché"""
        cache_key = f"report_{report_type}_{date_range[0]}_{date_range[1]}"
        cached_value = self.cache_manager.get(cache_key)
        if cached_value is not None:
            return pd.DataFrame(cached_value)

        if report_type == "Solicitudes":
            data = self._get_requests_data(date_range)
        elif report_type == "Certificados":
            data = self._get_certificates_data(date_range)
        else:
            data = self._get_ai_performance_data(date_range)

        return pd.DataFrame(data)

    def render(self) -> None:
        """Renderiza la interfaz del generador de reportes"""
        try:
            st.header("Generador de Reportes")

            # Configuración del reporte
            self._render_report_config()

            # Vista previa y descarga
            if st.session_state.report_data is not None:
                self._render_report_preview()
                self._render_download_options()

        except Exception as e:
            Logger.error(f"Error en generador de reportes: {str(e)}")
            st.error("Error generando el reporte")

    def _render_report_config(self) -> None:
        """Renderiza la configuración del reporte"""
        col1, col2 = st.columns(2)

        with col1:
            report_type = st.selectbox(
                "Tipo de Reporte",
                ["Solicitudes", "Certificados", "Rendimiento IA"],
                help="Seleccione el tipo de reporte a generar"
            )

        with col2:
            # Convertir datetime a date para el date_input
            default_start = (datetime.now() - timedelta(days=30)).date()
            default_end = datetime.now().date()

            # No anotamos el tipo aquí porque st.date_input retorna su propio tipo
            dates = st.date_input(
                "Rango de Fechas",
                value=(default_start, default_end),
                help="Seleccione el período para el reporte"
            )

            if st.button("Generar Reporte"):
                try:
                    # Validar y convertir las fechas
                    if isinstance(dates, (list, tuple)) and len(dates) == 2:
                        start_date = datetime.combine(dates[0], datetime.min.time())
                        end_date = datetime.combine(dates[1], datetime.max.time())
                        date_range = (start_date, end_date)
                        self._generate_report(report_type, date_range)
                    else:
                        st.error("Por favor seleccione un rango de fechas válido")

                except Exception as e:
                    Logger.error(f"Error procesando fechas: {str(e)}")
                    st.error("Error al procesar el rango de fechas")

    def _render_report_preview(self) -> None:
        """Renderiza vista previa del reporte"""
        st.subheader("Vista Previa")

        # Tabla de datos
        st.dataframe(
            st.session_state.report_data,
            use_container_width=True,
            hide_index=True
        )

        # Visualizaciones
        self._render_report_visualizations()

    def _render_report_visualizations(self) -> None:
        """Renderiza visualizaciones del reporte"""
        if st.session_state.last_report_type == "Solicitudes":
            fig = px.pie(
                st.session_state.report_data,
                names="status",
                title="Distribución por Estado"
            )
            st.plotly_chart(fig)

        elif st.session_state.last_report_type == "Certificados":
            fig = px.bar(
                st.session_state.report_data,
                x="created_at",
                y="count",
                title="Certificados por Fecha"
            )
            st.plotly_chart(fig)

    def _render_download_options(self) -> None:
        """Renderiza opciones de descarga"""
        col1, col2 = st.columns(2)

        with col1:
            self._download_csv()

        with col2:
            self._download_excel()

    def _generate_report(self, report_type: str, date_range: tuple) -> None:
        """Genera el reporte seleccionado"""
        try:
            st.session_state.report_data = self._get_report_data(
                report_type,
                date_range
            )
            st.session_state.last_report_type = report_type

        except Exception as e:
            Logger.error(f"Error generando reporte: {str(e)}")
            st.error("Error al generar el reporte")

    def _download_csv(self) -> None:
        """Descarga reporte en formato CSV"""
        if st.session_state.report_data is not None:
            csv = st.session_state.report_data.to_csv(index=False)
            st.download_button(
                "Descargar CSV",
                csv,
                "reporte.csv",
                "text/csv"
            )

    def _download_excel(self) -> None:
        """Descarga reporte en formato Excel"""
        if st.session_state.report_data is not None:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer) as writer:
                st.session_state.report_data.to_excel(writer, index=False)
            st.download_button(
                "Descargar Excel",
                buffer.getvalue(),
                "reporte.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    def _get_requests_data(self, date_range: Tuple[datetime, datetime]) -> List[Dict]:
        """Obtiene datos de solicitudes"""
        requests = self.solicitudes.get_requests()
        return [r for r in requests if date_range[0] <= r['created_at'] <= date_range[1]]

    def _get_certificates_data(self, date_range: Tuple[datetime, datetime]) -> List[Dict]:
        """Obtiene datos de certificados"""
        certificates = self.certificados.get_certificates()
        return [c for c in certificates if date_range[0] <= c['created_at'] <= date_range[1]]

    def _get_ai_performance_data(self, date_range: Tuple[datetime, datetime]) -> List[Dict]:
        """Obtiene datos de rendimiento de IA"""
        # Implementar lógica real aquí
        return []
