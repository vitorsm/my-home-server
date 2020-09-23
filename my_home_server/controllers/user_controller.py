
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

from my_home_server.controllers.errors_handler import fill_error_handlers_to_controller
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.user_service import UserService
import my_home_server.security.authentication_utils as authentication_utils

controller = Blueprint("user_controller", __name__, url_prefix="/api/user")
fill_error_handlers_to_controller(controller)


@controller.route("<path:user_id>")
@jwt_required()
@authentication_utils.set_authentication_context
def get_user(user_id: int, user_service: UserService, user_mapper: UserMapper):
    user = user_service.find_by_id(user_id)
    return jsonify(user_mapper.to_dto(user))


@controller.route("/")
@jwt_required()
@authentication_utils.set_authentication_context
def get_current_user(user_mapper: UserMapper):
    return jsonify(user_mapper.to_dto(AuthenticationContext.get_current_user()))


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
