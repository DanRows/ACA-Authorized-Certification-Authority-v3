import streamlit as st
from components.certificados import Certificados
from utils.helpers import validate_input
from datetime import datetime

def render_certificates():
    st.title("Gestión de Certificados")
    
    certificados = Certificados()
    
    # Formulario de generación
    with st.form("certificate_form"):
        st.header("Generar Nuevo Certificado")
        
        user_data = {
            "name": st.text_input("Nombre Completo"),
            "email": st.text_input("Correo Electrónico"),
            "type": st.selectbox(
                "Tipo de Certificado",
                ["Básico", "Avanzado", "Premium"]
            ),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        submitted = st.form_submit_button("Generar Certificado")
        
        if submitted:
            if validate_input(user_data, {
                "name": {"type": str},
                "email": {"type": str},
                "type": {"type": str}
            }):
                try:
                    result = certificados.generate_certificate(user_data)
                    st.success(f"Certificado generado: {result}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.error("Por favor complete todos los campos correctamente")
    
    # Lista de certificados
    st.header("Certificados Generados")
    cert_list = certificados.get_certificates()
    
    if cert_list:
        for cert in cert_list:
            with st.expander(f"Certificado {cert['id']}"):
                st.json(cert)
                if st.button(f"Descargar {cert['id']}", key=cert['id']):
                    certificados.download_certificate(cert['id'])
    else:
        st.info("No hay certificados generados") 