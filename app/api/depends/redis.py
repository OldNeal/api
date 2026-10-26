from app.redis.base import redis_client, redis

def get_redis() -> redis.Redis:
    return redis_client
