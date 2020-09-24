from typing import List, Optional

from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.generic_exception import GenericException


class InvalidDTOException(GenericException):

    required_fields: List[str]
    entity_name: str

    def __init__(self, error_code: ErrorCode, entity_name: str, required_fields: Optional[List[str]]):
        super().__init__(error_code, f"Failed to instantiate {entity_name}. "
                                     f"{f'Required fields: {str(required_fields)}' if required_fields else 'Null object'}")

        self.required_fields = required_fields
        self.entity_name = entity_name
