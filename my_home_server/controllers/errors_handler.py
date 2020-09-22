from flask import Blueprint, jsonify

from my_home_server.exceptions.api_error import APIError, APIErrorCode
from my_home_server.exceptions.permission_exception import PermissionException

import my_home_server.configs.log as log

logger = log.get_logger(__name__)


def fill_error_handlers_to_controller(controller: Blueprint):
    @controller.errorhandler(PermissionException)
    def permission_error(exception: PermissionException):
        logger.exception(exception)
        api_error = APIError(exception.error_code, None, str(exception))
        return jsonify(api_error.to_dto()), 403

    @controller.errorhandler(Exception)
    def generic_exception(exception: Exception):
        logger.exception(exception)
        api_error = APIError(APIErrorCode.GENERIC_EXCEPTION, None, "A generic exception occurred. Ask admin for help.")
        return jsonify(api_error.to_dto()), 500
