import streamlit as st
from components.solicitudes import Solicitudes
from utils.helpers import validate_input
import pandas as pd

def render_requests():
    st.title("Gestión de Solicitudes")
    
    solicitudes = Solicitudes()
    
    # Nueva solicitud
    with st.form("request_form"):
        st.header("Nueva Solicitud")
        
        request_data = {
            "name": st.text_input("Nombre del Solicitante"),
            "type": st.selectbox(
                "Tipo de Solicitud",
                ["certificate", "query", "support"]
            ),
            "description": st.text_area("Descripción")
        }
        
        submitted = st.form_submit_button("Enviar Solicitud")
        
        if submitted:
            if validate_input(request_data, {
                "name": {"type": str},
                "type": {"type": str},
                "description": {"type": str}
            }):
                result = solicitudes.add_request(request_data, request_data["type"])
                st.success(f"Solicitud creada: {result['request_id']}")
            else:
                st.error("Por favor complete todos los campos")
    
    # Lista de solicitudes
    st.header("Solicitudes Existentes")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.multiselect(
            "Estado",
            ["pending", "processing", "completed", "rejected"]
        )
    with col2:
        type_filter = st.multiselect(
            "Tipo",
            ["certificate", "query", "support"]
        )
    
    requests = solicitudes.get_requests()
    if requests:
        df = pd.DataFrame(requests)
        st.dataframe(df)
    else:
        st.info("No hay solicitudes registradas") 