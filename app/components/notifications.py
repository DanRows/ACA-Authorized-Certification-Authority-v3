import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from utils.logger import Logger
from utils.cache import cached

class Notifications:
    def __init__(self):
        self._initialize_state()
    
    def _initialize_state(self):
        """Inicializa el estado de las notificaciones"""
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        if 'last_notification_check' not in st.session_state:
            st.session_state.last_notification_check = datetime.now()
    
    def render(self):
        """Renderiza el panel de notificaciones"""
        try:
            st.subheader("Notificaciones")
            
            notifications = self._get_notifications()
            
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
                            self._mark_as_read(notification['id'])
            
        except Exception as e:
            Logger.error(f"Error en notificaciones: {str(e)}")
            st.error("Error cargando notificaciones")
    
    @cached(expire_in=60)
    def _get_notifications(self) -> List[Dict]:
        """Obtiene notificaciones con caché"""
        return sorted(
            st.session_state.notifications,
            key=lambda x: x['timestamp'],
            reverse=True
        )
    
    def add_notification(self, title: str, message: str):
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
            
        except Exception as e:
            Logger.error(f"Error agregando notificación: {str(e)}")
    
    def _mark_as_read(self, notification_id: int):
        """Marca una notificación como leída"""
        try:
            for notification in st.session_state.notifications:
                if notification['id'] == notification_id:
                    notification['read'] = True
                    break
                    
        except Exception as e:
            Logger.error(f"Error marcando notificación: {str(e)}")