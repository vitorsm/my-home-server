from typing import Optional

from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.user_group import UserGroup


class UserGroupMapper(MapperInterface):
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

    def validate_dto(self, dto: dict):
        self.generic_validate_dto(dto, ["name"], UserGroup.__name__)
