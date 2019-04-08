from src.base_app.services import redis


def save_pwd(login: str, pwd: str) -> bool:
    redis_connection = redis.connection()
    if not redis_connection:
        return False
    is_saved = redis_connection.set(login, pwd)

    return is_saved


def get_pwd(login: str) -> str:
    redis_connection = redis.connection()
    if not redis_connection:
        return ''
    pwd = redis_connection.get(login)
    if not pwd:
        return ''

    return pwd.decode()
