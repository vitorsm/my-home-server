
from flask import Blueprint, jsonify, request

from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.services.user_service import UserService

user_controller = Blueprint("user_controller", __name__, url_prefix="/api/user")


@user_controller.route("<path:user_id>")
def get_user(user_id: int, user_service: UserService, user_mapper: UserMapper):
    user = user_service.find_by_id(user_id)
    return jsonify(user_mapper.to_dto(user))
