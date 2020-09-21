from my_home_server.mappers.mapper import Mapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.user_group import UserGroup


class UserGroupMapper(MapperInterface):
    def to_dto(self, user_group: UserGroup) -> dict:
        return {
            "id": user_group.id,
            "name": user_group.name,
            "created_at": user_group.created_at,
            "description": user_group.description
        }

    def to_object(self, dto: dict) -> UserGroup:
        user_group = UserGroup()
        user_group.id = dto.get("id")
        user_group.name = dto.get("name")
        user_group.description = dto.get("description")

        return user_group

    def validate_dto(self, dto: dict):
        Mapper.validate_dto(dto, ["name"], UserGroup.__name__)