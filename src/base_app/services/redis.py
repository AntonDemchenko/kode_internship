import redis
from django.conf import settings
from rest_framework.response import Response


def connection():
    try:
        pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        redis_con = redis.Redis(connection_pool=pool)

        return redis_con

    except redis.ConnectionError:
        return Response(
            dict(
                code='validation_error',
                message='Check fields!'
            ),
            status=400
        )
