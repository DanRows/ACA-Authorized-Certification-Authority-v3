# app/main.py (ampliado)

import streamlit as st
from config.configuration import Configuration
from services.factory import ServiceFactory
from components.certificados import Certificados
from components.solicitudes import Solicitudes

def main():
    st.title("ACMA Dashboard")
    
    config = Configuration()
    provider = config.get_setting("default_provider")
    ai_service = ServiceFactory.create_service(provider)
    
    certificados = Certificados()
    solicitudes = Solicitudes()

    st.header("Certificate Generator")
    user_name = st.text_input("Enter your name")
    
    if st.button("Generate Certificate"):
        cert = certificados.generate_certificate({"name": user_name})
        st.success(cert)
    
    st.header("Requests Management")
    if st.button("Add Request"):
        result = solicitudes.add_request({"name": user_name}, "certificate")
        st.success(f"Request ID: {result['request_id']} added!")

    if st.button("Show All Requests"):
        st.json(solicitudes.get_requests())

if __name__ == "__main__":
    main()
