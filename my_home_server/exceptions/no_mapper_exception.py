from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.generic_exception import GenericException


class NoMapperException(GenericException):
    def __init__(self, entity_name):
        super().__init__(ErrorCode.NO_MAPPER_FOUND, f"Mapper not found to {entity_name}")
        self.entity_name = entity_name
