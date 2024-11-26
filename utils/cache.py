from functools import wraps
from datetime import datetime, timedelta
import json
import redis
from utils.logger import Logger

class Cache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        
    def set(self, key: str, value: any, expire_in: int = 3600):
        """
        Almacena un valor en caché
        
        Args:
            key: Clave para almacenar
            value: Valor a almacenar
        """
        try:
            serialized = json.dumps(value)
            self.redis_client.setex(key, expire_in, serialized)
        except Exception as e:
            Logger.error(f"Error al almacenar en caché: {e}")
    
    def get(self, key: str) -> any:
        """
        Recupera un valor de la caché
        
        Args:
            key: Clave a recuperar
            
        Returns:
            El valor almacenado o None si no existe
        """
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            Logger.error(f"Error al recuperar de caché: {e}")
            return None

def cached(expire_in=3600):
    """
    Decorador para cachear resultados de funciones
    
    Args:
        expire_in: Tiempo de expiración en segundos
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = Cache()
            
            # Genera clave única para la función y sus argumentos
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Intenta obtener resultado de caché
            result = cache.get(key)
            if result is not None:
                return result
            
            # Si no está en caché, ejecuta la función
            result = func(*args, **kwargs)
            cache.set(key, result, expire_in)
            return result
        return wrapper
    return decorator 