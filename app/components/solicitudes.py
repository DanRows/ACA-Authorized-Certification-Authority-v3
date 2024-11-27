from datetime import datetime
from typing import Dict, List, Optional

from app.utils.logger import Logger


class Solicitudes:
    def __init__(self):
        self._requests: List[Dict] = []

    def get_total(self) -> int:
        return len(self._requests)

    def get_requests(self) -> List[Dict]:
        return self._requests

    def add_request(self, request: Dict) -> None:
        try:
            request['created_at'] = datetime.now()
            self._requests.append(request)
            Logger.info(f"Solicitud agregada: {request.get('id', 'unknown')}")
        except Exception as e:
            Logger.error(f"Error al agregar solicitud: {str(e)}")
            raise

    def get_request_by_id(self, request_id: str) -> Optional[Dict]:
        try:
            return next(
                (req for req in self._requests if req['id'] == request_id),
                None
            )
        except Exception as e:
            Logger.error(f"Error al buscar solicitud {request_id}: {str(e)}")
            return None

    def get_provider_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas por proveedor"""
        try:
            providers = {}
            for request in self._requests:
                provider = request.get('provider', 'unknown')
                providers[provider] = providers.get(provider, 0) + 1
            return providers
        except Exception as e:
            Logger.error(f"Error obteniendo estadísticas de proveedores: {str(e)}")
            return {}
