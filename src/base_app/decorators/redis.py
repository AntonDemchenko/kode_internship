import redis
from django.conf import settings
from rest_framework.response import Response


def redis_connection(fn):
    def _wrapper(request, *args, **kwargs):
        try:
            redis_con = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB
            )
            return fn(request, redis_con=redis_con, *args, **kwargs)
            redis_con.close()
        except redis.ConnectionError:
            return Response(
                dict(
                    code='validation_error',
                    message='Check fields!'
                ),
                status=400
            )

    return _wrapper
