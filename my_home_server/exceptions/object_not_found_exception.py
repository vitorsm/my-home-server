from typing import Optional

from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.generic_exception import GenericException


class ObjectNotFoundException(GenericException):
    def __init__(self, error_code: ErrorCode, entity_name: str, entity_identifier: Optional[dict]):
        super().__init__(error_code, f"{entity_name} not found. "
                                     f"{f'Identifier: {str(entity_identifier)}' if entity_identifier else 'No identifier'}")
        self.entity_name = entity_name
        self.entity_identifier = entity_identifier
