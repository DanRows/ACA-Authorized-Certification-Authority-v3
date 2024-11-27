import os
from typing import Optional

from app.utils.logger import Logger


class SecretsManager:
    """
    Gestiona el acceso seguro a credenciales y secretos.
    """

    @staticmethod
    def get_secret(key: str) -> Optional[str]:
        """
        Obtiene un secreto desde las variables de entorno.

        Args:
            key (str): La clave del secreto a obtener.

        Returns:
            Optional[str]: El valor del secreto o None si no se encuentra.
        """
        try:
            return os.getenv(key)
        except Exception as e:
            Logger.error(f"Error obteniendo secreto {key}: {str(e)}")
            return None

    @staticmethod
    def set_secret(key: str, value: str) -> bool:
        """
        Establece un secreto en las variables de entorno.

        Args:
            key (str): La clave del secreto.
            value (str): El valor del secreto.

        Returns:
            bool: True si se estableció correctamente, False en caso contrario.
        """
        try:
            os.environ[key] = value
            return True
        except Exception as e:
            Logger.error(f"Error estableciendo secreto {key}: {str(e)}")
            return False

    @staticmethod
    def delete_secret(key: str) -> bool:
        """
        Elimina un secreto de las variables de entorno.

        Args:
            key (str): La clave del secreto a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        try:
            if key in os.environ:
                del os.environ[key]
                return True
            return False
        except Exception as e:
            Logger.error(f"Error eliminando secreto {key}: {str(e)}")
            return False
