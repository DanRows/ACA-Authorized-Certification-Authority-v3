"""
Páginas del ACMA Dashboard
-------------------------
Este paquete contiene las páginas principales de la aplicación.
"""

from app.pages.home import HomePage, render_home_page
from app.pages.settings import SettingsPage

__all__ = [
    'HomePage',
    'render_home_page',
    'SettingsPage'
]
