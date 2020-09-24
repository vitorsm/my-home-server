from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.generic_exception import GenericException


class DuplicateEntryException(GenericException):
    def __init__(self, error_code: ErrorCode, entity: str, field: str, value: str):
        super().__init__(error_code, f"Cannot create {entity} because the field {field} is unique and the value "
                                     f"{value} already exists")
        self.entity = entity
        self.field = field
        self.value = value
