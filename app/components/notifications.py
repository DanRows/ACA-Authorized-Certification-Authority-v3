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

    def render(self) -> None:
        """Renderiza el panel de notificaciones"""
        try:
            st.subheader("Notificaciones")

            notifications = self.get_notifications()

            if not notifications:
                st.info("No hay notificaciones nuevas")
                return

            for notification in notifications:
                with st.expander(
                    f"{notification['title']} - {notification['timestamp'].strftime('%H:%M')}",
                    expanded=not notification['read']
                ):
                    st.write(notification['message'])
                    if not notification['read']:
                        if st.button("Marcar como leída", key=f"mark_read_{notification['id']}"):
                            self.mark_as_read(notification['id'])
                            st.rerun()

        except Exception as e:
            Logger.error(f"Error en notificaciones: {str(e)}")
            st.error("Error cargando notificaciones")

    def add_notification(self, title: str, message: str) -> None:
        """
        Agrega una nueva notificación.

        Args:
            title: Título de la notificación
            message: Contenido de la notificación
        """
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
        """
        Obtiene todas las notificaciones.

        Returns:
            List[Dict]: Lista de notificaciones ordenadas por fecha
        """
        return sorted(
            st.session_state.notifications,
            key=lambda x: x['timestamp'],
            reverse=True
        )

    def mark_as_read(self, notification_id: int) -> None:
        """
        Marca una notificación como leída.

        Args:
            notification_id: ID de la notificación a marcar
        """
        try:
            for notification in st.session_state.notifications:
                if notification['id'] == notification_id:
                    notification['read'] = True
                    Logger.info(f"Notificación {notification_id} marcada como leída")
                    break
        except Exception as e:
            Logger.error(f"Error marcando notificación como leída: {str(e)}")

    def get_unread_count(self) -> int:
        """
        Obtiene el número de notificaciones no leídas.

        Returns:
            int: Número de notificaciones sin leer
        """
        try:
            return len([n for n in st.session_state.notifications if not n['read']])
        except Exception as e:
            Logger.error(f"Error contando notificaciones no leídas: {str(e)}")
            return 0

    def clear_all(self) -> None:
        """Elimina todas las notificaciones"""
        try:
            st.session_state.notifications = []
            Logger.info("Todas las notificaciones eliminadas")
        except Exception as e:
            Logger.error(f"Error eliminando notificaciones: {str(e)}")
