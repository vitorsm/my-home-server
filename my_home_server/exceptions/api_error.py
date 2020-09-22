from dataclasses import dataclass
from enum import Enum
from typing import Optional


class APIErrorCode(Enum):
    UPDATE_USER_PERMISSION = 4002

    GENERIC_EXCEPTION = 5001


@dataclass
class APIError(object):
    error_code: APIErrorCode
    title: Optional[str]
    message: str

    def to_dto(self):
        return {
            "error_code": self.error_code.value,
            "title": self.title if self.title else self.error_code.name,
            "message": self.message
        }
