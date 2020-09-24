from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.generic_exception import GenericException


class NoCommitFunctionFoundException(GenericException):
    def __init__(self, service_name: str):
        super().__init__(ErrorCode.NO_COMMIT_FUNCTION_FOUND,
                         f"try to commit transaction but {service_name} service has no function commit")
        self.service_name = service_name
