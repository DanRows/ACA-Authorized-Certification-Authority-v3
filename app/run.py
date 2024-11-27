import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Agregar el directorio raíz al PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from app.main import main  # noqa: E402

if __name__ == "__main__":
    try:
        # Cambiar al directorio del proyecto
        os.chdir(root_dir)

        load_dotenv()
        st.set_page_config(
            page_title="ACMA Dashboard",
            page_icon="📊",
            layout="wide"
        )
        main()
    except Exception as e:
        st.error(f"Error iniciando la aplicación: {str(e)}")
