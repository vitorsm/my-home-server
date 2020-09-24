from enum import Enum
from typing import Optional

from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.generic_exception import GenericException


class Actions(Enum):
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    GET = 4


class PermissionException(GenericException):
    def __init__(self, error_code: ErrorCode, entity: Optional[str], action: Optional[Actions]):
        super().__init__(error_code, f"You don't have permission to "
                                     f"{action.name if action else 'perform this action in'} this "
                                     f"{entity if entity else 'object'}")
        self.entity = entity
        self.action = action
        self.error_code = error_code
