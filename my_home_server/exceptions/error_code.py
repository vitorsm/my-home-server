from enum import Enum


class ErrorCode(Enum):
    UPDATE_USER_PERMISSION = 4002
    USER_LOGIN_ALREADY_EXISTS = 4003

    GENERIC_EXCEPTION = 5001
