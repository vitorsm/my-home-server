from datetime import datetime
from typing import Optional

from my_home_server.dao.user_dao import UserDAO
from my_home_server.exceptions.authentication_exception import AuthenticationException
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.user import User


class UserService(object):
    user_dao: UserDAO

    def __init__(self):
        self.mapper = Mapper.get_mapper(User.__name__)

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.user_dao.find_by_id(user_id)

    def authenticate(self, login: str, password: str) -> User:
        user = self.user_dao.find_by_credentials(login, password)

        if not user:
            raise AuthenticationException(login)

        return user

    def create_user(self, dto: dict):
        self.mapper.validate_dto(dto)

        user = self.mapper.to_object(dto)
        user.created_at = datetime.utcnow()

        self.user_dao.add(user)

        return user

    def update_user(self, dto: dict):
        self.mapper.validate_dto(dto)

        user = self.find_by_id(dto.get("id"))

        if not user:
            raise ObjectNotFoundException(User.__name__, {"id": dto.get("id")})

        self.mapper.to_object(dto, user)

        self.user_dao.commit()
