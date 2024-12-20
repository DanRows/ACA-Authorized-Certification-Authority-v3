"""
Páginas del ACMA Dashboard
-------------------------
Este paquete contiene las páginas principales de la aplicación.
"""

from app.pages.certificates import CertificatesPage, render_certificates_page
from app.pages.home import HomePage, render_home_page
from app.pages.requests import RequestsPage, render_requests_page
from app.pages.settings import SettingsPage

__all__ = [
    'CertificatesPage',
    'render_certificates_page',
    'HomePage',
    'render_home_page',
    'RequestsPage',
    'render_requests_page',
    'SettingsPage'
]
