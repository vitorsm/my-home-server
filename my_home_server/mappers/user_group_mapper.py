from typing import Optional

from my_home_server.dao.user_group_dao import UserGroupDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.user_group import UserGroup


class UserGroupMapper(MapperInterface):
    def __init__(self, user_group_dao: UserGroupDAO):
        self.user_group_dao = user_group_dao

    def get_error_code_when_dto_invalid_to_insert(self):
        return ErrorCode.INVALID_INPUT_CREATE_USER_GROUP

    def get_error_code_when_dto_invalid_to_update(self):
        return ErrorCode.INVALID_INPUT_UPDATE_USER_GROUP

    def to_dto(self, user_group: UserGroup) -> Optional[dict]:
        if not user_group:
            return None

        return {
            "id": user_group.id,
            "name": user_group.name,
            "created_at": user_group.created_at,
            "description": user_group.description
        }

    def to_object(self, dto: dict, not_update: bool = False) -> Optional[UserGroup]:
        if not dto:
            return None

        user_group = None
        found = False
        if dto.get("id"):
            user_group = self.user_group_dao.find_by_id(dto.get("id"))
            found = user_group is not None

        if not found:
            user_group = UserGroup()
            user_group.id = dto.get("id")

        if not found or not not_update:
            user_group.name = dto.get("name")
            user_group.description = dto.get("description")

        return user_group

    def get_required_fields_to_insert(self):
        return ["name"]

    def get_required_fields_to_update(self):
        return ["id", "name"]

    def get_entity_name(self):
        return UserGroup.__name__
