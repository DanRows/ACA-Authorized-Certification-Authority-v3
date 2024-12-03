from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.database import Client, ClientStatus, Equipment


class AnalyticsDashboard:
    def __init__(self, db_session: Session):
        self.db = db_session

    def render_client_metrics(self):
        """Renderiza métricas de clientes"""
        try:
            # Total de clientes
            total_clients = self.db.query(Client).count()
            active_clients = self.db.query(Client).filter(
                Client.status == ClientStatus.ACTIVE
            ).count()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Clientes", total_clients)
            with col2:
                st.metric("Clientes Activos", active_clients)
            with col3:
                satisfaction = self.db.query(
                    func.avg(Client.satisfaction_score)
                ).scalar() or 0.0
                st.metric("Satisfacción Promedio", f"{satisfaction:.1f}/5.0")

            # Gráfico de satisfacción
            satisfaction_data = [
                r[0] for r in self.db.query(Client.satisfaction_score).all()
                if r[0] is not None
            ]
            if satisfaction_data:
                fig = px.histogram(
                    satisfaction_data,
                    title="Distribución de Satisfacción"
                )
                st.plotly_chart(fig)
            else:
                st.info("No hay datos de satisfacción disponibles")

        except Exception as e:
            st.error(f"Error mostrando métricas de clientes: {str(e)}")

    def render_equipment_metrics(self):
        """Renderiza métricas de equipos"""
        try:
            # Total equipos calibrados
            total_equipment = self.db.query(Equipment).count()
            calibrated = self.db.query(Equipment).filter(
                Equipment.calibration_date > datetime.now() - timedelta(days=365)
            ).count()

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Equipos", total_equipment)
            with col2:
                st.metric("Calibrados (último año)", calibrated)

            # Gráfico de calibraciones por mes
            calibration_data = self.db.query(
                func.strftime('%Y-%m', Equipment.calibration_date).label('month'),
                func.count(Equipment.id).label('count')
            ).group_by('month').all()

            if calibration_data:
                fig = go.Figure(data=[
                    go.Bar(
                        x=[d[0] for d in calibration_data],
                        y=[d[1] for d in calibration_data]
                    )
                ])
                fig.update_layout(title="Calibraciones por Mes")
                st.plotly_chart(fig)
            else:
                st.info("No hay datos de calibración disponibles")

        except Exception as e:
            st.error(f"Error mostrando métricas de equipos: {str(e)}")
