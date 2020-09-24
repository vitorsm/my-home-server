from typing import Optional

from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.user_group import UserGroup


class UserGroupMapper(MapperInterface):

    def get_error_code_when_dto_invalid_to_insert(self):
        return ErrorCode.GENERIC_EXCEPTION

    def get_error_code_when_dto_invalid_to_update(self):
        return ErrorCode.GENERIC_EXCEPTION

    def to_dto(self, user_group: UserGroup) -> Optional[dict]:
        if not user_group:
            return None

        return {
            "id": user_group.id,
            "name": user_group.name,
            "created_at": user_group.created_at,
            "description": user_group.description
        }

    def to_object(self, dto: dict, loaded_object: UserGroup = None) -> Optional[UserGroup]:
        if not dto:
            return None

        user_group = loaded_object if loaded_object else UserGroup()
        user_group.id = dto.get("id")
        user_group.name = dto.get("name")
        user_group.description = dto.get("description")

        return user_group

    def get_required_fields_to_insert(self):
        return ["name"]

    def get_required_fields_to_update(self):
        return ["id", "name"]

    def get_entity_name(self):
        return UserGroup.__name__
