from datetime import datetime, timedelta
from typing import Dict, List, Optional

from app.utils.logger import Logger


class Solicitudes:
    def __init__(self):
        self._requests: List[Dict] = []
        self._initialize_sample_data()

    def _initialize_sample_data(self) -> None:
        """Inicializa datos de ejemplo"""
        if not self._requests:
            self._requests = [
                {
                    'id': 'REQ001',
                    'client': 'Laboratorio Central',
                    'contact': 'Juan Pérez',
                    'email': 'jperez@lab.com',
                    'phone': '555-0101',
                    'service_type': 'Calibración de Balanzas',
                    'urgency': 'Normal',
                    'location': 'Laboratorio PROCyMI',
                    'equipment': {
                        'type': 'Balanza Analítica',
                        'brand': 'Mettler Toledo',
                        'model': 'XPE205',
                        'serial': 'B123456789',
                        'last_calibration': datetime.now() - timedelta(days=365)
                    },
                    'requirements': {
                        'needs_adjustment': True,
                        'needs_maintenance': False,
                        'iso_required': True,
                        'express_service': False
                    },
                    'status': 'pending',
                    'created_at': datetime.now() - timedelta(days=2),
                    'desired_date': datetime.now() + timedelta(days=5)
                },
                {
                    'id': 'REQ002',
                    'client': 'Hospital Regional',
                    'contact': 'María García',
                    'email': 'mgarcia@hospital.com',
                    'phone': '555-0202',
                    'service_type': 'Calibración de Termómetros',
                    'urgency': 'Urgente',
                    'location': 'Instalaciones del Cliente',
                    'equipment': {
                        'type': 'Termómetro Digital',
                        'brand': 'Fluke',
                        'model': '1523',
                        'serial': 'T987654321',
                        'last_calibration': datetime.now() - timedelta(days=180)
                    },
                    'requirements': {
                        'needs_adjustment': False,
                        'needs_maintenance': True,
                        'iso_required': True,
                        'express_service': True
                    },
                    'status': 'in_progress',
                    'created_at': datetime.now() - timedelta(days=1),
                    'started_at': datetime.now() - timedelta(hours=4),
                    'desired_date': datetime.now() + timedelta(days=2)
                },
                {
                    'id': 'REQ003',
                    'client': 'Industria Farmacéutica',
                    'contact': 'Carlos López',
                    'email': 'clopez@farma.com',
                    'phone': '555-0303',
                    'service_type': 'Calibración de Material Volumétrico',
                    'urgency': 'Normal',
                    'location': 'Laboratorio PROCyMI',
                    'equipment': {
                        'type': 'Material Volumétrico',
                        'brand': 'Brand',
                        'model': 'Volumetric Flask',
                        'serial': 'V456789123',
                        'last_calibration': None
                    },
                    'requirements': {
                        'needs_adjustment': False,
                        'needs_maintenance': False,
                        'iso_required': True,
                        'express_service': False
                    },
                    'status': 'completed',
                    'created_at': datetime.now() - timedelta(days=10),
                    'completed_at': datetime.now() - timedelta(days=8),
                    'desired_date': datetime.now() - timedelta(days=7)
                },
                {
                    'id': 'REQ004',
                    'client': 'Universidad Nacional',
                    'contact': 'Ana Martínez',
                    'email': 'amartinez@uni.edu',
                    'phone': '555-0404',
                    'service_type': 'Calibración de Balanzas',
                    'urgency': 'Normal',
                    'location': 'Laboratorio PROCyMI',
                    'equipment': {
                        'type': 'Balanza de Precisión',
                        'brand': 'Sartorius',
                        'model': 'Quintix224-1S',
                        'serial': 'B789123456',
                        'last_calibration': datetime.now() - timedelta(days=400)
                    },
                    'requirements': {
                        'needs_adjustment': True,
                        'needs_maintenance': True,
                        'iso_required': False,
                        'express_service': False
                    },
                    'status': 'approved',
                    'created_at': datetime.now() - timedelta(hours=12),
                    'approved_at': datetime.now() - timedelta(hours=6),
                    'desired_date': datetime.now() + timedelta(days=10)
                },
                {
                    'id': 'REQ005',
                    'client': 'Laboratorio Clínico',
                    'contact': 'Roberto Sánchez',
                    'email': 'rsanchez@lab.com',
                    'phone': '555-0505',
                    'service_type': 'Calibración de Higrómetros',
                    'urgency': 'Urgente',
                    'location': 'Instalaciones del Cliente',
                    'equipment': {
                        'type': 'Higrómetro',
                        'brand': 'Testo',
                        'model': '608-H1',
                        'serial': 'H321654987',
                        'last_calibration': datetime.now() - timedelta(days=300)
                    },
                    'requirements': {
                        'needs_adjustment': False,
                        'needs_maintenance': False,
                        'iso_required': True,
                        'express_service': True
                    },
                    'status': 'rejected',
                    'created_at': datetime.now() - timedelta(days=5),
                    'rejected_at': datetime.now() - timedelta(days=4),
                    'rejection_reason': 'Equipo no cumple requisitos mínimos',
                    'desired_date': datetime.now() + timedelta(days=3)
                }
            ]

    def get_total(self) -> int:
        """
        Obtiene el total de solicitudes.

        Returns:
            int: Número total de solicitudes
        """
        return len(self._requests)

    def get_requests(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Obtiene la lista de solicitudes.

        Args:
            limit: Límite opcional de solicitudes a retornar

        Returns:
            List[Dict]: Lista de solicitudes
        """
        try:
            requests = sorted(
                self._requests,
                key=lambda x: x['created_at'],
                reverse=True
            )
            return requests[:limit] if limit else requests
        except Exception as e:
            Logger.error(f"Error obteniendo solicitudes: {str(e)}")
            return []

    def add_request(self, request: Dict) -> None:
        """
        Agrega una nueva solicitud.

        Args:
            request: Datos de la solicitud a agregar
        """
        try:
            if 'created_at' not in request:
                request['created_at'] = datetime.now()
            if 'status' not in request:
                request['status'] = 'pending'
            self._requests.append(request)
            Logger.info(f"Solicitud agregada: {request.get('id', 'unknown')}")
        except Exception as e:
            Logger.error(f"Error al agregar solicitud: {str(e)}")
            raise

    def get_request_by_id(self, request_id: str) -> Optional[Dict]:
        """
        Busca una solicitud por su ID.

        Args:
            request_id: ID de la solicitud a buscar

        Returns:
            Optional[Dict]: Solicitud encontrada o None si no existe
        """
        try:
            for request in self._requests:
                if request['id'] == request_id:
                    return request
            return None
        except Exception as e:
            Logger.error(f"Error buscando solicitud {request_id}: {str(e)}")
            return None

    def update_request(self, request_id: str, updates: Dict) -> bool:
        """
        Actualiza una solicitud existente.

        Args:
            request_id: ID de la solicitud a actualizar
            updates: Datos a actualizar

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            for request in self._requests:
                if request['id'] == request_id:
                    request.update(updates)
                    Logger.info(f"Solicitud {request_id} actualizada")
                    return True
            return False
        except Exception as e:
            Logger.error(f"Error actualizando solicitud {request_id}: {str(e)}")
            return False

    def delete_request(self, request_id: str) -> bool:
        """
        Elimina una solicitud.

        Args:
            request_id: ID de la solicitud a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            initial_length = len(self._requests)
            self._requests = [
                req for req in self._requests
                if req['id'] != request_id
            ]
            deleted = len(self._requests) < initial_length
            if deleted:
                Logger.info(f"Solicitud {request_id} eliminada")
            return deleted
        except Exception as e:
            Logger.error(f"Error eliminando solicitud {request_id}: {str(e)}")
            return False

    def get_status_stats(self) -> Dict[str, int]:
        """
        Obtiene estadísticas por estado.

        Returns:
            Dict[str, int]: Diccionario con conteo por estado
        """
        try:
            stats = {}
            for request in self._requests:
                status = request.get('status', 'unknown')
                stats[status] = stats.get(status, 0) + 1
            return stats
        except Exception as e:
            Logger.error(f"Error obteniendo estadísticas de estados: {str(e)}")
            return {}

    def get_urgency_stats(self) -> Dict[str, int]:
        """
        Obtiene estadísticas por urgencia.

        Returns:
            Dict[str, int]: Diccionario con conteo por nivel de urgencia
        """
        try:
            stats = {}
            for request in self._requests:
                urgency = request.get('urgency', 'unknown')
                stats[urgency] = stats.get(urgency, 0) + 1
            return stats
        except Exception as e:
            Logger.error(f"Error obteniendo estadísticas de urgencia: {str(e)}")
            return {}

    def get_service_type_stats(self) -> Dict[str, int]:
        """
        Obtiene estadísticas por tipo de servicio.

        Returns:
            Dict[str, int]: Diccionario con conteo por tipo de servicio
        """
        try:
            stats = {}
            for request in self._requests:
                service_type = request.get('service_type', 'unknown')
                stats[service_type] = stats.get(service_type, 0) + 1
            return stats
        except Exception as e:
            Logger.error(f"Error obteniendo estadísticas de servicios: {str(e)}")
            return {}
