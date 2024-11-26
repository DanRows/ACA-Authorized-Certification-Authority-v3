import streamlit as st
from datetime import datetime
from utils.logger import Logger

class Notifications:
    def __init__(self):
        self._initialize_session_state()
        
    def _initialize_session_state(self):
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
            
    def add_notification(self, message, type="info"):
        """
        Agrega una nueva notificación al sistema.
        """
        notification = {
            "message": message,
            "type": type,
            "timestamp": datetime.now(),
            "read": False
        }
        st.session_state.notifications.insert(0, notification)
        
    def render(self):
        """
        Muestra las notificaciones en la interfaz.
        """
        with st.sidebar.expander("Notificaciones", expanded=True):
            unread = len([n for n in st.session_state.notifications if not n["read"]])
            
            if unread > 0:
                st.markdown(f"**{unread} nuevas notificaciones**")
            
            for idx, notif in enumerate(st.session_state.notifications[:5]):
                self._render_notification(idx, notif)
                
    def _render_notification(self, idx, notification):
        with st.container():
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                if notification["type"] == "error":
                    st.error(notification["message"])
                elif notification["type"] == "warning":
                    st.warning(notification["message"])
                else:
                    st.info(notification["message"])
                    
            with col2:
                if not notification["read"]:
                    if st.button("✓", key=f"notif_{idx}"):
                        st.session_state.notifications[idx]["read"] = True
                        st.experimental_rerun() 