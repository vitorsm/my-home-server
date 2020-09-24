from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.generic_exception import GenericException


class AuthenticationException(GenericException):
    def __init__(self, error_code: ErrorCode, login: str):
        super().__init__(error_code, f"Authentication failed for {login}")
        self.login = login
