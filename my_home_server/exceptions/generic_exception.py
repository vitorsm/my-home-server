from typing import Optional

from my_home_server.exceptions.error_code import ErrorCode

INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error.  Ask admin for help."


class GenericException(Exception):
    error_code: ErrorCode
    title: Optional[str]
    message: str
    description: Optional[dict]

    def __init__(self, error_code: ErrorCode, message: str, title: Optional[str] = None,
                 description: Optional[dict] = None):
        super().__init__(f"{error_code.name} - {message}")

        self.error_code = error_code
        self.message = message
        self.title = title
        self.description = description

    def to_dto(self, fill_description: bool = True):
        return {
            "error_code": self.error_code.value,
            "title": self.get_title(),
            "message": self.__get_message(),
            "description": self.__get_description() if fill_description else None
        }

    def get_title(self):
        return self.title if self.title else self.error_code.name

    def __get_description(self):
        if self.__is_internal_error():
            return None

        if self.description:
            return self.description

        complete_dto = self.__dict__
        generic_dto = self.to_dto(fill_description=False)
        description = dict()

        for field, value in complete_dto.items():
            if field not in generic_dto:
                description.update({field: value})

        return description

    def __get_message(self):
        if self.__is_internal_error():
            return INTERNAL_SERVER_ERROR_MESSAGE
        else:
            return self.message

    def __is_internal_error(self):
        return str(self.error_code.value).startswith("500")

    def get_http_status(self) -> int:
        return int(str(self.error_code.value)[:3])
