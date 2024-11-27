from datetime import datetime
from typing import Dict, List, Optional

from app.utils.logger import Logger


class Solicitudes:
    def __init__(self):
        self._requests: List[Dict] = []

    def get_total(self) -> int:
        """
        Obtiene el total de solicitudes.

        Returns:
            int: Número total de solicitudes
        """
        return len(self._requests)

    def get_requests(self) -> List[Dict]:
        """
        Obtiene todas las solicitudes.

        Returns:
            List[Dict]: Lista de solicitudes
        """
        try:
            return sorted(
                self._requests,
                key=lambda x: x['created_at'],
                reverse=True
            )
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
            return next(
                (req for req in self._requests if req['id'] == request_id),
                None
            )
        except Exception as e:
            Logger.error(f"Error al buscar solicitud {request_id}: {str(e)}")
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

    def get_provider_stats(self) -> Dict[str, int]:
        """
        Obtiene estadísticas por proveedor.

        Returns:
            Dict[str, int]: Diccionario con conteo por proveedor
        """
        try:
            stats = {}
            for request in self._requests:
                provider = request.get('provider', 'unknown')
                stats[provider] = stats.get(provider, 0) + 1
            return stats
        except Exception as e:
            Logger.error(f"Error obteniendo estadísticas de proveedores: {str(e)}")
            return {}
