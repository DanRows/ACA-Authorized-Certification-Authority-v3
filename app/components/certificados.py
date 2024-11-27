from datetime import datetime
from typing import Dict, List, Optional

from app.utils.logger import Logger


class Certificados:
    def __init__(self):
        self._certificates: List[Dict] = []

    def get_total(self) -> int:
        return len(self._certificates)

    def get_certificates(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Obtiene la lista de certificados
        Args:
            limit: Límite opcional de certificados a retornar
        """
        try:
            if limit is not None:
                return sorted(
                    self._certificates,
                    key=lambda x: x['created_at'],
                    reverse=True
                )[:limit]
            return self._certificates
        except Exception as e:
            Logger.error(f"Error obteniendo certificados: {str(e)}")
            return []

    def add_certificate(self, certificate: Dict) -> None:
        try:
            certificate['created_at'] = datetime.now()
            self._certificates.append(certificate)
            Logger.info(f"Certificado agregado: {certificate['id']}")
        except Exception as e:
            Logger.error(f"Error al agregar certificado: {str(e)}")
            raise

    def get_certificate_by_id(self, certificate_id: str) -> Optional[Dict]:
        try:
            return next(
                (cert for cert in self._certificates if cert['id'] == certificate_id),
                None
            )
        except Exception as e:
            Logger.error(f"Error al buscar certificado {certificate_id}: {str(e)}")
            return None
