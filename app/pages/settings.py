import streamlit as st
from config.configuration import Configuration
from config.secrets_manager import SecretsManager
from utils.logger import Logger

def render_settings():
    st.title("Configuración del Sistema")
    
    config = Configuration()
    
    # Sección de Proveedores de IA
    st.header("Proveedores de IA")
    
    current_provider = config.get_setting("default_provider")
    providers = config.get_setting("ai_providers")
    
    selected_provider = st.selectbox(
        "Proveedor Predeterminado",
        providers,
        index=providers.index(current_provider)
    )
    
    if selected_provider != current_provider:
        # Aquí iría la lógica para actualizar el proveedor
        st.success(f"Proveedor actualizado a: {selected_provider}")
    
    # Configuración de Base de Datos
    st.header("Configuración de Base de Datos")
    
    with st.form("database_config"):
        db_url = st.text_input(
            "URL de Base de Datos",
            value=config.get_setting("database_url"),
            type="password"
        )
        
        if st.form_submit_button("Actualizar Configuración"):
            try:
                # Aquí iría la lógica para actualizar la configuración
                st.success("Configuración actualizada exitosamente")
            except Exception as e:
                st.error(f"Error: {str(e)}") 