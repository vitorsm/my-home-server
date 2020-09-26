
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

import my_home_server.security.authentication_utils as authentication_utils
import my_home_server.controllers.errors_handler as errors_handler

from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.user_service import UserService

controller = Blueprint("user_controller", __name__, url_prefix="/api/user")
errors_handler.fill_error_handlers_to_controller(controller)


@controller.route("<path:user_id>")
@jwt_required()
@authentication_utils.set_authentication_context
def get_user(user_id: str, user_service: UserService, user_mapper: UserMapper):
    user = user_service.find_by_id(int(user_id))
    return jsonify(user_mapper.to_dto(user))


@controller.route("/", methods=['POST'])
def create_user(user_service: UserService, user_mapper: UserMapper):
    user_dto = request.json
    user = user_service.create_from_dto(user_dto)
    return jsonify(user_mapper.to_dto(user))


@controller.route("/", methods=['PUT'])
@jwt_required()
@authentication_utils.set_authentication_context
def update_user(user_service: UserService, user_mapper: UserMapper):
    user_dto = request.json
    user = user_service.update_from_dto(user_dto)
    return jsonify(user_mapper.to_dto(user))


@controller.route("/", methods=['GET'])
def get_current_user(user_mapper: UserMapper):
    return jsonify(user_mapper.to_dto(AuthenticationContext.get_current_user()))
