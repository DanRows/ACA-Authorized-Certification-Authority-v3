from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

import redis

from utils.logger import Logger


class CacheManager:
    def __init__(self):
        self.redis_client = self._initialize_redis()
        self.local_cache = {}

    def _initialize_redis(self) -> Optional[redis.Redis]:
        try:
            return redis.Redis(
                host='localhost',
                port=6379,
                db=0,
                decode_responses=True,
                socket_timeout=2
            )
        except Exception as e:
            Logger.warning(f"Redis no disponible: {e}")
            return None

    def _get_from_redis(self, key: str) -> Any:
        if self.redis_client is None:
            return None
        try:
            value = self.redis_client.get(key)
            return value if value else None
        except Exception as e:
            Logger.error(f"Error al obtener de Redis: {e}")
            return None

    def _get_from_local(self, key: str) -> Any:
        return self.local_cache.get(key)

    def get(self, key: str) -> Any:
        redis_value = self._get_from_redis(key)
        if redis_value is not None:
            return redis_value
        return self._get_from_local(key)


def cached(ttl: int = 3600) -> Callable:
    """
    Decorador para cachear resultados de funciones
    Args:
        ttl: Tiempo de vida del caché en segundos
    """
    cache: Dict = {}

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = str((func.__name__, args, frozenset(kwargs.items())))
            now = datetime.now()

            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < timedelta(seconds=ttl):
                    return result

            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result

        return wrapper

    return decorator
