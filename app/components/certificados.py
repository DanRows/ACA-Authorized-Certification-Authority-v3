from datetime import datetime, timedelta
from typing import Dict, List, Optional

from app.utils.logger import Logger


class Certificados:
    def __init__(self):
        self._certificates: List[Dict] = []
        self._initialize_sample_data()

    def _initialize_sample_data(self) -> None:
        """Inicializa datos de ejemplo"""
        if not self._certificates:
            self._certificates = [
                {
                    'id': 'CERT001',
                    'client': 'Laboratorio Central',
                    'type': 'Balanza Analítica',
                    'calibration_date': datetime.now() - timedelta(days=30),
                    'next_calibration': datetime.now() + timedelta(days=335),
                    'status': 'active',
                    'created_at': datetime.now() - timedelta(days=30),
                    'details': {
                        'brand': 'Mettler Toledo',
                        'model': 'XPE205',
                        'serial': 'B123456789',
                        'measurement_range': '0.1mg - 220g',
                        'resolution': '0.01mg',
                        'location': 'Laboratorio PROCyMI',
                        'standard': 'OIML R76',
                        'environmental_conditions': {
                            'temperature': 20.1,
                            'humidity': 45.5,
                            'pressure': 1013.25
                        },
                        'observations': 'Calibración rutinaria'
                    }
                },
                {
                    'id': 'CERT002',
                    'client': 'Hospital Regional',
                    'type': 'Termómetro Digital',
                    'calibration_date': datetime.now() - timedelta(days=15),
                    'next_calibration': datetime.now() + timedelta(days=350),
                    'status': 'active',
                    'created_at': datetime.now() - timedelta(days=15),
                    'details': {
                        'brand': 'Fluke',
                        'model': '1523',
                        'serial': 'T987654321',
                        'measurement_range': '-30°C a 150°C',
                        'resolution': '0.001°C',
                        'location': 'Instalaciones del Cliente',
                        'standard': 'ISO/IEC 17025:2017',
                        'environmental_conditions': {
                            'temperature': 21.2,
                            'humidity': 48.0,
                            'pressure': 1012.8
                        },
                        'observations': 'Calibración in situ'
                    }
                },
                {
                    'id': 'CERT003',
                    'client': 'Industria Farmacéutica',
                    'type': 'Material Volumétrico',
                    'calibration_date': datetime.now() - timedelta(days=60),
                    'next_calibration': datetime.now() - timedelta(days=5),
                    'status': 'expired',
                    'created_at': datetime.now() - timedelta(days=60),
                    'details': {
                        'brand': 'Brand',
                        'model': 'Volumetric Flask',
                        'serial': 'V456789123',
                        'measurement_range': '100mL',
                        'resolution': '0.1mL',
                        'location': 'Laboratorio PROCyMI',
                        'standard': 'ISO/IEC 17025:2017',
                        'environmental_conditions': {
                            'temperature': 20.5,
                            'humidity': 47.0,
                            'pressure': 1013.0
                        },
                        'observations': 'Calibración de material clase A'
                    }
                },
                {
                    'id': 'CERT004',
                    'client': 'Universidad Nacional',
                    'type': 'Balanza de Precisión',
                    'calibration_date': datetime.now() - timedelta(days=5),
                    'next_calibration': datetime.now() + timedelta(days=360),
                    'status': 'active',
                    'created_at': datetime.now() - timedelta(days=5),
                    'details': {
                        'brand': 'Sartorius',
                        'model': 'Quintix224-1S',
                        'serial': 'B789123456',
                        'measurement_range': '0.1mg - 220g',
                        'resolution': '0.1mg',
                        'location': 'Laboratorio PROCyMI',
                        'standard': 'OIML R76',
                        'environmental_conditions': {
                            'temperature': 20.3,
                            'humidity': 46.5,
                            'pressure': 1013.1
                        },
                        'observations': 'Calibración post mantenimiento'
                    }
                },
                {
                    'id': 'CERT005',
                    'client': 'Laboratorio Clínico',
                    'type': 'Higrómetro',
                    'calibration_date': datetime.now() - timedelta(days=45),
                    'next_calibration': datetime.now() + timedelta(days=25),
                    'status': 'active',
                    'created_at': datetime.now() - timedelta(days=45),
                    'details': {
                        'brand': 'Testo',
                        'model': '608-H1',
                        'serial': 'H321654987',
                        'measurement_range': '10% a 95% HR',
                        'resolution': '0.1% HR',
                        'location': 'Instalaciones del Cliente',
                        'standard': 'ISO/IEC 17025:2017',
                        'environmental_conditions': {
                            'temperature': 20.8,
                            'humidity': 47.5,
                            'pressure': 1012.9
                        },
                        'observations': 'Calibración para área de control de calidad'
                    }
                }
            ]

    def get_total(self) -> int:
        """
        Obtiene el total de certificados.

        Returns:
            int: Número total de certificados
        """
        return len(self._certificates)

    def get_certificates(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Obtiene la lista de certificados.

        Args:
            limit: Límite opcional de certificados a retornar

        Returns:
            List[Dict]: Lista de certificados
        """
        try:
            certificates = sorted(
                self._certificates,
                key=lambda x: x['created_at'],
                reverse=True
            )
            return certificates[:limit] if limit else certificates
        except Exception as e:
            Logger.error(f"Error obteniendo certificados: {str(e)}")
            return []

    def add_certificate(self, certificate: Dict) -> None:
        """
        Agrega un nuevo certificado.

        Args:
            certificate: Datos del certificado a agregar
        """
        try:
            if 'created_at' not in certificate:
                certificate['created_at'] = datetime.now()
            if 'status' not in certificate:
                certificate['status'] = 'pending'
            self._certificates.append(certificate)
            Logger.info(f"Certificado agregado: {certificate.get('id', 'unknown')}")
        except Exception as e:
            Logger.error(f"Error al agregar certificado: {str(e)}")
            raise

    def get_certificate_by_id(self, certificate_id: str) -> Optional[Dict]:
        """
        Busca un certificado por su ID.

        Args:
            certificate_id: ID del certificado a buscar

        Returns:
            Optional[Dict]: Certificado encontrado o None si no existe
        """
        try:
            return next(
                (cert for cert in self._certificates if cert['id'] == certificate_id),
                None
            )
        except Exception as e:
            Logger.error(f"Error al buscar certificado {certificate_id}: {str(e)}")
            return None

    def update_certificate(self, certificate_id: str, updates: Dict) -> bool:
        """
        Actualiza un certificado existente.

        Args:
            certificate_id: ID del certificado a actualizar
            updates: Datos a actualizar

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            for cert in self._certificates:
                if cert['id'] == certificate_id:
                    cert.update(updates)
                    Logger.info(f"Certificado {certificate_id} actualizado")
                    return True
            return False
        except Exception as e:
            Logger.error(f"Error actualizando certificado {certificate_id}: {str(e)}")
            return False

    def delete_certificate(self, certificate_id: str) -> bool:
        """
        Elimina un certificado.

        Args:
            certificate_id: ID del certificado a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            initial_length = len(self._certificates)
            self._certificates = [
                cert for cert in self._certificates
                if cert['id'] != certificate_id
            ]
            deleted = len(self._certificates) < initial_length
            if deleted:
                Logger.info(f"Certificado {certificate_id} eliminado")
            return deleted
        except Exception as e:
            Logger.error(f"Error eliminando certificado {certificate_id}: {str(e)}")
            return False

    def get_status_stats(self) -> Dict[str, int]:
        """
        Obtiene estadísticas por estado.

        Returns:
            Dict[str, int]: Diccionario con conteo por estado
        """
        try:
            stats = {}
            for cert in self._certificates:
                status = cert.get('status', 'unknown')
                stats[status] = stats.get(status, 0) + 1
            return stats
        except Exception as e:
            Logger.error(f"Error obteniendo estadísticas de estados: {str(e)}")
            return {}
