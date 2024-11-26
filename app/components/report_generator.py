import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.metrics import Metrics
from utils.helpers import format_date
import plotly.express as px

class ReportGenerator:
    def __init__(self):
        self.metrics = Metrics()
        
    def render(self):
        st.header("Generador de Reportes")
        
        # Configuración del reporte
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox(
                "Tipo de Reporte",
                ["Solicitudes", "Certificados", "Rendimiento IA"]
            )
            
        with col2:
            date_range = st.date_input(
                "Rango de Fechas",
                value=(
                    datetime.now() - timedelta(days=30),
                    datetime.now()
                )
            )
        
        if st.button("Generar Reporte"):
            self._generate_report(report_type, date_range)
    
    def _generate_report(self, report_type, date_range):
        try:
            if report_type == "Solicitudes":
                self._generate_requests_report(date_range)
            elif report_type == "Certificados":
                self._generate_certificates_report(date_range)
            else:
                self._generate_ai_performance_report(date_range)
                
            # Opción de descarga
            st.download_button(
                "Descargar Reporte",
                self._get_report_data(),
                f"reporte_{report_type.lower()}_{datetime.now().strftime('%Y%m%d')}.csv"
            )
            
        except Exception as e:
            st.error(f"Error generando reporte: {str(e)}")
    
    def _get_report_data(self):
        # Aquí iría la lógica real de exportación
        return "datos,del,reporte" 