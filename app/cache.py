import redis
from app.config import get_settings

settings = get_settings()
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def get_cached_value(key: str) -> str | None:
    return redis_client.get(key)


def set_cached_value(key: str, value: str, ttl_seconds: int = 3600) -> None:
    redis_client.set(name=key, value=value, ex=ttl_seconds)