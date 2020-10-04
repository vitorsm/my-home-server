from typing import Optional

from my_home_server.dao.user_dao import UserDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.user_group_mapper import UserGroupMapper
from my_home_server.models.user import User


class UserMapper(MapperInterface):
    def __init__(self, user_dao: UserDAO, user_group_mapper: UserGroupMapper):
        self.user_dao = user_dao
        self.user_group_mapper = user_group_mapper

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

    def to_object(self, user_dto: dict, not_update: bool = False) -> Optional[User]:
        if not user_dto:
            return None

        user = None
        found = False

        if user_dto.get("id"):
            user = self.user_dao.find_by_id(user_dto.get("id"))
            found = user is not None

        if not found:
            user = User()
            user.id = user_dto.get("id")
            user.login = user_dto.get("login")
            user.created_at = user_dto.get("created_at")

        if not found or not not_update:
            user.name = user_dto.get("name")

            if user_dto.get("user_group"):
                user.user_group = self.user_group_mapper.to_object(user_dto.get("user_group"), not_update=True)

            if user_dto.get("password"):
                user.password = user_dto.get("password")

        return user

    def get_required_fields_to_insert(self):
        return ["name", "login", "password"]

    def get_required_fields_to_update(self):
        return ["id", "login", "name"]

    def get_entity_name(self):
        return User.__name__
