from enum import Enum
from typing import Optional

from my_home_server.exceptions.api_error import APIErrorCode


class Actions(Enum):
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    GET = 4


class PermissionException(Exception):
    def __init__(self, error_code: APIErrorCode, entity: Optional[str], action: Optional[Actions]):
        super().__init__(f"You don't have permission to {action.name if action else 'perform this action in'} this "
                         f"{entity if entity else 'object'}")
        self.entity = entity
        self.action = action
        self.error_code = error_code
