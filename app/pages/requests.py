from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
import streamlit as st

from app.components.notifications import Notifications
from app.components.solicitudes import Solicitudes
from app.utils.cache import cached
from app.utils.logger import Logger


class RequestsPage:
    def __init__(self):
        self.solicitudes = Solicitudes()
        self.notifications = Notifications()
        self._initialize_state()

    def _initialize_state(self) -> None:
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

    def render(self) -> None:
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

    @cached(ttl=300)
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

    def _render_filters(self) -> None:
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

    def _render_requests_list(self) -> None:
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

    def _render_request_details(self) -> None:
        """Renderiza detalles de una solicitud"""
        request = st.session_state.selected_request
        st.subheader(f"Solicitud #{request['id']}")

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Estado: {request['status']}")
            st.write(f"Fecha: {request['created_at']}")
        with col2:
            st.write(f"Proveedor: {request.get('provider', 'N/A')}")

        # Acciones
        if st.button("Marcar como Completada"):
            self.solicitudes.update_request(request['id'], {"status": "completed"})
            st.success("Solicitud actualizada")
            st.rerun()

    def _render_statistics(self) -> None:
        """Renderiza estadísticas de solicitudes"""
        requests = self._get_filtered_requests()

        if not requests:
            return

        st.subheader("Estadísticas")

        # Gráfico de estado
        status_counts = pd.DataFrame(requests)['status'].value_counts()
        st.bar_chart(status_counts)


def render_requests_page():
    """Punto de entrada para la página de solicitudes"""
    page = RequestsPage()
    page.render()
