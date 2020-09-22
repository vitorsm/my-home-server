from dataclasses import dataclass

from typing import Optional

from my_home_server.exceptions.error_code import ErrorCode


@dataclass
class APIError(object):
    error_code: ErrorCode
    title: Optional[str]
    message: str

    def to_dto(self):
        return {
            "error_code": self.error_code.value,
            "title": self.title if self.title else self.error_code.name,
            "message": self.message
        }
