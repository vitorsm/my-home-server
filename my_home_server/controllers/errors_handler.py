from flask import Blueprint, jsonify
from flask_jwt import JWTError

from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.generic_exception import GenericException

import my_home_server.configs.log as log

logger = log.get_logger(__name__)


def fill_error_handlers_to_controller(controller: Blueprint):

    @controller.errorhandler(JWTError)
    def jwt_error(exception: JWTError):
        logger.exception(exception)

        api_error = None
        error_code = ErrorCode.AUTHENTICATION_REQUIRED

        if exception.description == "Signature has expired":
            error_code = ErrorCode.EXPIRED_TOKEN_ERROR
        elif exception.error == "Invalid token":
            error_code = ErrorCode.INVALID_TOKEN_ERROR

        if not api_error:
            api_error = GenericException(error_code, str(exception.description))

        return jsonify(api_error.to_dto()), api_error.get_http_status()

    @controller.errorhandler(GenericException)
    def duplicate_entry_exception(exception: GenericException):
        logger.exception(exception)
        return jsonify(exception.to_dto()), exception.get_http_status()

    @controller.errorhandler(Exception)
    def generic_exception(exception: Exception):
        logger.exception(exception)
        api_error = GenericException(ErrorCode.GENERIC_EXCEPTION, "A generic exception occurred. Ask admin for help.")
        return jsonify(api_error.to_dto()), api_error.get_http_status()
