import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.solicitudes import Solicitudes
from utils.helpers import validate_input
from utils.logger import Logger
from utils.cache import cached
from components.notifications import Notifications

class RequestsPage:
    def __init__(self):
        self.solicitudes = Solicitudes()
        self.notifications = Notifications()
        self._initialize_state()
    
    def _initialize_state(self):
        """Inicializa el estado de la página"""
        if 'requests_filter' not in st.session_state:
            st.session_state.requests_filter = "all"
        if 'date_range' not in st.session_state:
            st.session_state.date_range = (
                datetime.now() - timedelta(days=30),
                datetime.now()
            )
        if 'selected_request' not in st.session_state:
            st.session_state.selected_request = None
    
    def render(self):
        """Renderiza la página de solicitudes"""
        try:
            st.title("Gestión de Solicitudes")
            
            # Filtros y controles
            self._render_filters()
            
            # Vista principal
            col1, col2 = st.columns([2, 1])
            
            with col1:
                self._render_requests_list()
            
            with col2:
                if st.session_state.selected_request:
                    self._render_request_details()
                else:
                    self._render_statistics()
            
        except Exception as e:
            Logger.error(f"Error en página de solicitudes: {str(e)}")
            st.error("Error cargando solicitudes")
    
    @cached(expire_in=300)
    def _get_filtered_requests(self) -> List[Dict]:
        """Obtiene solicitudes filtradas con caché"""
        try:
            status = st.session_state.requests_filter
            date_range = st.session_state.date_range
            
            requests = self.solicitudes.get_requests()
            filtered = [
                r for r in requests
                if (status == "all" or r["status"] == status) and
                date_range[0] <= r["created_at"] <= date_range[1]
            ]
            return filtered
            
        except Exception as e:
            Logger.error(f"Error filtrando solicitudes: {str(e)}")
            return []
    
    def _render_filters(self):
        """Renderiza filtros de solicitudes"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.requests_filter = st.selectbox(
                "Estado",
                ["all", "pending", "completed", "rejected"],
                format_func=lambda x: {
                    "all": "Todas",
                    "pending": "Pendientes",
                    "completed": "Completadas",
                    "rejected": "Rechazadas"
                }[x]
            )
        
        with col2:
            st.session_state.date_range = st.date_input(
                "Rango de Fechas",
                value=st.session_state.date_range
            )
    
    def _render_actions(self):
        """Renderiza acciones principales"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Nueva Solicitud"):
                self._create_new_request()
        
        with col2:
            if st.button("Exportar Datos"):
                self._export_requests()
        
        with col3:
            if st.button("Actualizar"):
                st.experimental_rerun()
    
    def _render_requests_list(self):
        """Renderiza lista de solicitudes"""
        requests = self._get_filtered_requests()
        
        if not requests:
            st.info("No se encontraron solicitudes con los filtros actuales")
            return
        
        df = pd.DataFrame(requests)
        st.dataframe(
            df,
            column_config={
                "created_at": st.column_config.DatetimeColumn("Fecha"),
                "status": st.column_config.SelectboxColumn(
                    "Estado",
                    options=["pending", "completed", "rejected"]
                )
            },
            hide_index=True
        )
    
    def _render_statistics(self):
        """Renderiza estadísticas de solicitudes"""
        requests = self._get_filtered_requests()
        
        if not requests:
            return
            
        st.subheader("Estadísticas")
        
        # Gráfico de estado
        fig = px.pie(
            pd.DataFrame(requests),
            names="status",
            title="Distribución por Estado"
        )
        st.plotly_chart(fig)
    
    def _create_new_request(self):
        """Crea una nueva solicitud"""
        try:
            result = self.solicitudes.add_request({
                "created_at": datetime.now(),
                "status": "pending"
            })
            self.notifications.add_notification(
                f"Nueva solicitud creada: #{result['request_id']}",
                "success"
            )
        except Exception as e:
            Logger.error(f"Error creando solicitud: {str(e)}")
            st.error("Error creando la solicitud")
    
    def _export_requests(self):
        """Exporta las solicitudes filtradas"""
        try:
            requests = self._get_filtered_requests()
            df = pd.DataFrame(requests)
            csv = df.to_csv(index=False)
            
            st.download_button(
                "Descargar CSV",
                csv,
                f"solicitudes_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        except Exception as e:
            Logger.error(f"Error exportando solicitudes: {str(e)}")
            st.error("Error exportando las solicitudes")

def render_requests_page():
    """Punto de entrada para la página de solicitudes"""
    page = RequestsPage()
    page.render() 