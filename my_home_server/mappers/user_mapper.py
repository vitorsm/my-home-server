from typing import Optional

from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.user_group_mapper import UserGroupMapper
from my_home_server.models.user import User


class UserMapper(MapperInterface):
    def __init__(self):
        self.user_group_mapper = UserGroupMapper()

    def get_error_code_when_dto_invalid_to_insert(self):
        return ErrorCode.INVALID_INPUT_CREATE_USER

    def get_error_code_when_dto_invalid_to_update(self):
        return ErrorCode.INVALID_INPUT_UPDATE_USER

    def to_dto(self, user: User) -> Optional[dict]:
        if not user:
            return None

        return {
            "id": user.id,
            "name": user.name,
            "login": user.login,
            "password": None,
            "user_group": self.user_group_mapper.to_dto(user.user_group),
            "created_at": user.created_at
        }

    def to_object(self, user_dto: dict, loaded_object: User = None) -> Optional[User]:
        if not user_dto:
            return None

        user = loaded_object if loaded_object else User()
        user.id = user_dto.get("id")
        user.name = user_dto.get("name")
        user.login = user_dto.get("login") if not loaded_object else loaded_object.login

        if not loaded_object:
            user.created_at = user_dto.get("created_at")
            user.password = user_dto.get("password")

        return user

    def get_required_fields_to_insert(self):
        return ["name", "login", "password"]

    def get_required_fields_to_update(self):
        return ["id", "login", "name"]

    def get_entity_name(self):
        return User.__name__
