import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Agregar el directorio raíz al PYTHONPATH
project_dir = Path(__file__).parent.parent.absolute()
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# Ahora podemos importar desde app
from app.main import main

if __name__ == "__main__":
    try:
        # Cambiar al directorio del proyecto
        os.chdir(project_dir)

        # Cargar variables de entorno
        load_dotenv()

        # Configurar Streamlit
        st.set_page_config(
            page_title="ACMA Dashboard",
            page_icon="📊",
            layout="wide"
        )

        # Ejecutar la aplicación
        main()
    except Exception as e:
        st.error(f"Error iniciando la aplicación: {str(e)}")
