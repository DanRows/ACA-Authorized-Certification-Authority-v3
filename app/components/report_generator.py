import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import plotly.express as px

from utils.logger import Logger
from utils.cache import cached
from components.metrics import Metrics
from components.solicitudes import Solicitudes
from components.certificados import Certificados

class ReportGenerator:
    def __init__(self):
        self.metrics = Metrics()
        self.solicitudes = Solicitudes()
        self.certificados = Certificados()
        self._initialize_state()
    
    def _initialize_state(self):
        """Inicializa el estado del generador de reportes"""
        if 'report_data' not in st.session_state:
            st.session_state.report_data = None
        if 'last_report_type' not in st.session_state:
            st.session_state.last_report_type = None
    
    @cached(expire_in=300)
    def _get_report_data(self, report_type: str, date_range: Tuple[datetime, datetime]) -> pd.DataFrame:
        """Obtiene datos del reporte con caché"""
        if report_type == "Solicitudes":
            return self._get_requests_data(date_range)
        elif report_type == "Certificados":
            return self._get_certificates_data(date_range)
        else:
            return self._get_ai_performance_data(date_range)
    
    def render(self):
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
    
    def _render_report_config(self):
        """Renderiza la configuración del reporte"""
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox(
                "Tipo de Reporte",
                ["Solicitudes", "Certificados", "Rendimiento IA"],
                help="Seleccione el tipo de reporte a generar"
            )
            
        with col2:
            date_range = st.date_input(
                "Rango de Fechas",
                value=(
                    datetime.now() - timedelta(days=30),
                    datetime.now()
                ),
                help="Seleccione el período para el reporte"
            )
        
        if st.button("Generar Reporte"):
            self._generate_report(report_type, date_range)
    
    def _render_report_preview(self):
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
    
    def _render_report_visualizations(self):
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
    
    def _render_download_options(self):
        """Renderiza opciones de descarga"""
        col1, col2 = st.columns(2)
        
        with col1:
            self._download_csv()
        
        with col2:
            self._download_excel()
    
    def _generate_report(self, report_type: str, date_range: tuple):
        """Genera el reporte seleccionado"""
        try:
            st.session_state.report_data = self._get_report_data(
                report_type, 
                date_range
            )
            st.session_state.last_report_type = report_type
            
        except Exception as e:
            Logger.error(f"Error generando reporte: {str(e)}")
            st.error("Error generando el reporte")
    
    def _download_csv(self):
        """Opción de descarga CSV"""
        if st.session_state.report_data is not None:
            csv = st.session_state.report_data.to_csv(index=False)
            st.download_button(
                "Descargar CSV",
                csv,
                f"reporte_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    def _download_excel(self):
        """Opción de descarga Excel"""
        if st.session_state.report_data is not None:
            buffer = pd.ExcelWriter('report.xlsx', engine='xlsxwriter')
            st.session_state.report_data.to_excel(buffer, index=False)
            st.download_button(
                "Descargar Excel",
                buffer,
                f"reporte_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )