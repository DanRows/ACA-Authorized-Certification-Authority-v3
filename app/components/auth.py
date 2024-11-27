from typing import Dict, Optional

import streamlit as st

from utils.logger import Logger


class Auth:
    def __init__(self):
        self._users = {
            "admin": "admin123"  # En producción usar hash seguro
        }

    def login(self, username: str, password: str) -> bool:
        try:
            if username in self._users and self._users[username] == password:
                st.session_state.authenticated = True
                Logger.info(f"Usuario {username} autenticado")
                return True
            return False
        except Exception as e:
            Logger.error(f"Error en login: {str(e)}")
            return False

    def logout(self) -> None:
        try:
            st.session_state.authenticated = False
            Logger.info("Usuario desconectado")
        except Exception as e:
            Logger.error(f"Error en logout: {str(e)}")

    def is_authenticated(self) -> bool:
        return st.session_state.get('authenticated', False)
