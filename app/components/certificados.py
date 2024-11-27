from datetime import datetime
from typing import Dict, List, Optional

from app.utils.logger import Logger


class Certificados:
    def __init__(self):
        self._certificates: List[Dict] = []

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
