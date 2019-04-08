import redis
from django.conf import settings


def connection():
    pool = redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    redis_con = redis.Redis(connection_pool=pool)

    return redis_con
