from functools import wraps

from my_home_server.exceptions.authentication_exception import AuthenticationException
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.user_service import UserService
from flask_jwt import current_identity, JWTError


def authenticate(login: str, password: str, user_service: UserService):
    try:
        return user_service.authenticate(login, password)
    except AuthenticationException as exception:
        raise JWTError(exception.get_title(), exception.message)


def identity(payload: dict, user_service: UserService):
    user_id = payload.get("identity")
    return user_service.find_by_id(user_id)


def set_authentication_context(function):
    @wraps(function)
    def function_wrapper(*args, **kwargs):
        AuthenticationContext.init_context(current_identity)
        return function(*args, **kwargs)

    return function_wrapper
