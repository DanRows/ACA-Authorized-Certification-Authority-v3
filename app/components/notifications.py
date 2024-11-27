from datetime import datetime
from typing import Dict, List, Optional

import streamlit as st

from app.utils.logger import Logger


class Notifications:
    def __init__(self):
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Inicializa el estado de las notificaciones"""
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        if 'last_notification_check' not in st.session_state:
            st.session_state.last_notification_check = datetime.now()

    def add_notification(self, title: str, message: str) -> None:
        """Agrega una nueva notificación"""
        try:
            notification = {
                'id': len(st.session_state.notifications),
                'title': title,
                'message': message,
                'timestamp': datetime.now(),
                'read': False
            }
            st.session_state.notifications.append(notification)
            Logger.info(f"Nueva notificación agregada: {title}")
        except Exception as e:
            Logger.error(f"Error agregando notificación: {str(e)}")

    def get_notifications(self) -> List[Dict]:
        """Obtiene todas las notificaciones"""
        return sorted(
            st.session_state.notifications,
            key=lambda x: x['timestamp'],
            reverse=True
        )

    def mark_as_read(self, notification_id: int) -> None:
        """Marca una notificación como leída"""
        try:
            for notification in st.session_state.notifications:
                if notification['id'] == notification_id:
                    notification['read'] = True
                    break
        except Exception as e:
            Logger.error(f"Error marcando notificación como leída: {str(e)}")
