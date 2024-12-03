from datetime import datetime
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
                        'model': 'XA 220/X',
                        'serial': 'BAL-001'
                    },
                    'requirements': {
                        'needs_adjustment': True,
                        'needs_maintenance': False,
                        'iso_required': True,
                        'express_service': False
                    },
                    'status': 'pending',
                    'created_at': datetime.now()
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
                        'model': 'DT-01',
                        'serial': 'TERM-001'
                    },
                    'requirements': {
                        'needs_adjustment': False,
                        'needs_maintenance': True,
                        'iso_required': True,
                        'express_service': True
                    },
                    'status': 'in_progress',
                    'created_at': datetime.now()
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
