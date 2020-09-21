from my_home_server.mappers.mapper import Mapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.user import User


class UserMapper(MapperInterface):

    def to_dto(self, user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "login": user.login,
            "password": None,
            "user_group": {},
            "created_at": user.created_at
        }

    def to_object(self, user_dto: dict, loaded_object: User = None) -> User:
        user = loaded_object if loaded_object else User()
        user.id = user_dto.get("id")
        user.name = user_dto.get("name")
        user.login = user_dto.get("login")
        user.password = user_dto.get("password")
        user.user_group = None

        if not loaded_object:
            user.created_at = user_dto.get("created_at")

        return user

    def validate_dto(self, dto: dict):
        Mapper.validate_dto(dto, ["name", "login", "password"], User.__name__)
