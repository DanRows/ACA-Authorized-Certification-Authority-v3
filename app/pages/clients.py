from datetime import datetime
from typing import Dict, List

import pandas as pd
import plotly.express as px
import streamlit as st

from app.utils.logger import Logger


class ClientsPage:
    def __init__(self):
        self._initialize_state()
        self._load_sample_data()

    def _initialize_state(self) -> None:
        """Inicializa el estado de la página"""
        if 'clients' not in st.session_state:
            st.session_state.clients = []
        if 'editing_client' not in st.session_state:
            st.session_state.editing_client = None

    def _load_sample_data(self) -> None:
        """Carga datos de ejemplo si no hay datos"""
        if not st.session_state.clients:
            st.session_state.clients = [
                {
                    'id': 'CLI001',
                    'name': 'Laboratorio Central',
                    'contact': 'Juan Pérez',
                    'email': 'jperez@lab.com',
                    'phone': '555-0101',
                    'address': 'Av. Principal 123',
                    'type': 'Laboratorio',
                    'created_at': datetime.now(),
                    'status': 'active',
                    'equipment': [
                        {
                            'type': 'Balanza',
                            'model': 'XA 220/X',
                            'serial': 'BAL-001'
                        }
                    ]
                },
                {
                    'id': 'CLI002',
                    'name': 'Hospital Regional',
                    'contact': 'María García',
                    'email': 'mgarcia@hospital.com',
                    'phone': '555-0202',
                    'address': 'Calle Salud 456',
                    'type': 'Salud',
                    'created_at': datetime.now(),
                    'status': 'active',
                    'equipment': [
                        {
                            'type': 'Termómetro',
                            'model': 'DT-01',
                            'serial': 'TERM-001'
                        }
                    ]
                }
            ]

    def render(self) -> None:
        """Renderiza la página de gestión de clientes"""
        try:
            st.title("Gestión de Clientes")

            # Tabs para diferentes secciones
            tab1, tab2, tab3 = st.tabs([
                "👥 Clientes",
                "➕ Nuevo Cliente",
                "📊 Análisis"
            ])

            with tab1:
                self._render_clients_list()
            with tab2:
                self._render_new_client_form()
            with tab3:
                self._render_clients_analysis()

        except Exception as e:
            Logger.error(f"Error en página de clientes: {str(e)}")
            st.error("Error cargando clientes")

    def _render_clients_list(self) -> None:
        """Renderiza lista de clientes"""
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("🔍 Buscar cliente", key="client_search")
        with col2:
            type_filter = st.multiselect(
                "Tipo de Cliente",
                ["Laboratorio", "Salud", "Industrial", "Educación", "Otro"]
            )

        # Aplicar filtros
        filtered_clients = st.session_state.clients
        if search:
            filtered_clients = [
                c for c in filtered_clients
                if search.lower() in c['name'].lower() or
                search.lower() in c['contact'].lower()
            ]
        if type_filter:
            filtered_clients = [
                c for c in filtered_clients
                if c['type'] in type_filter
            ]

        # Mostrar clientes
        for client in filtered_clients:
            with st.expander(f"🏢 {client['name']}", expanded=False):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**ID:** {client['id']}")
                    st.write(f"**Contacto:** {client['contact']}")
                    st.write(f"**Email:** {client['email']} | **Tel:** {client['phone']}")
                    st.write(f"**Dirección:** {client['address']}")
                    st.write(f"**Tipo:** {client['type']}")

                    # Equipos del cliente
                    if client.get('equipment'):
                        st.write("**Equipos:**")
                        for eq in client['equipment']:
                            st.write(f"- {eq['type']} | Modelo: {eq['model']} | Serie: {eq['serial']}")

                with col2:
                    if st.button("📝 Editar", key=f"edit_{client['id']}"):
                        st.session_state.editing_client = client['id']
                    if st.button("❌ Eliminar", key=f"delete_{client['id']}"):
                        st.session_state.clients = [
                            c for c in st.session_state.clients
                            if c['id'] != client['id']
                        ]
                        st.success("Cliente eliminado")
                        st.rerun()

    def _render_new_client_form(self) -> None:
        """Renderiza formulario de nuevo cliente"""
        with st.form("new_client"):
            st.subheader("Registro de Cliente")

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nombre/Razón Social")
                contact = st.text_input("Persona de Contacto")
                email = st.text_input("Email")
            with col2:
                phone = st.text_input("Teléfono")
                address = st.text_input("Dirección")
                client_type = st.selectbox(
                    "Tipo de Cliente",
                    ["Laboratorio", "Salud", "Industrial", "Educación", "Otro"]
                )

            # Equipos del cliente
            st.subheader("Equipos del Cliente")
            col1, col2, col3 = st.columns(3)
            with col1:
                eq_type = st.selectbox(
                    "Tipo de Equipo",
                    ["Balanza", "Termómetro", "Material Volumétrico", "Higrómetro"]
                )
            with col2:
                eq_model = st.text_input("Modelo")
            with col3:
                eq_serial = st.text_input("Número de Serie")

            if st.form_submit_button("Registrar Cliente"):
                try:
                    new_client = {
                        'id': f'CLI{len(st.session_state.clients) + 1:03d}',
                        'name': name,
                        'contact': contact,
                        'email': email,
                        'phone': phone,
                        'address': address,
                        'type': client_type,
                        'created_at': datetime.now(),
                        'status': 'active',
                        'equipment': [
                            {
                                'type': eq_type,
                                'model': eq_model,
                                'serial': eq_serial
                            }
                        ] if eq_model and eq_serial else []
                    }
                    st.session_state.clients.append(new_client)
                    st.success("✅ Cliente registrado exitosamente")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al registrar cliente: {str(e)}")

    def _render_clients_analysis(self) -> None:
        """Renderiza análisis de clientes"""
        if not st.session_state.clients:
            st.info("No hay datos para analizar")
            return

        # Convertir a DataFrame
        df = pd.DataFrame(st.session_state.clients)

        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Clientes", len(df))
        with col2:
            active = len(df[df['status'] == 'active'])
            st.metric("Clientes Activos", active)
        with col3:
            with_equipment = len([
                c for c in st.session_state.clients
                if c.get('equipment')
            ])
            st.metric("Con Equipos", with_equipment)

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            # Distribución por tipo
            fig = px.pie(
                df,
                names='type',
                title="Distribución por Tipo de Cliente"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Equipos por tipo
            equipment_types = []
            for client in st.session_state.clients:
                for eq in client.get('equipment', []):
                    equipment_types.append(eq['type'])

            if equipment_types:
                eq_df = pd.DataFrame({'type': equipment_types})
                fig = px.bar(
                    eq_df['type'].value_counts().reset_index(),
                    x='index',
                    y='type',
                    title="Equipos por Tipo"
                )
                st.plotly_chart(fig, use_container_width=True)


def render_clients_page():
    """Punto de entrada para la página de clientes"""
    try:
        page = ClientsPage()
        page.render()
    except Exception as e:
        Logger.error(f"Error en página de clientes: {str(e)}")
        st.error("Error cargando la página de clientes")
