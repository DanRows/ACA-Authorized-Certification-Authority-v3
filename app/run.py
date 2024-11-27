import os

import streamlit as st
from dotenv import load_dotenv

from app.main import main

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        load_dotenv()
        st.set_page_config(
            page_title="ACMA Dashboard",
            page_icon="📊",
            layout="wide"
        )
        main()
    except Exception as e:
        st.error(f"Error iniciando la aplicación: {str(e)}")
