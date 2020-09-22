from datetime import datetime
from typing import Optional

from my_home_server.dao.user_dao import UserDAO
from my_home_server.exceptions.authentication_exception import AuthenticationException
from my_home_server.exceptions.duplicate_entry_exception import DuplicateEntryException
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.exceptions.permission_exception import PermissionException, Actions
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.security.password_encryption import PasswordEncryption
from my_home_server.services.user_group_service import UserGroupService


class UserService(object):
    def __init__(self, user_dao: UserDAO, user_group_service: UserGroupService):
        self.user_dao = user_dao
        self.user_group_service = user_group_service
        self.mapper = Mapper.get_mapper(User.__name__)

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.user_dao.find_by_id(user_id)

    def authenticate(self, login: str, password: str) -> User:
        user = self.user_dao.find_by_login(login)

        if not user or not PasswordEncryption.check_encrypted_password(password, user.password):
            raise AuthenticationException(login)

        return user

    def create_by_dto(self, dto: dict):
        self.mapper.validate_dto(dto)

        user = self.mapper.to_object(dto)
        user.created_at = datetime.utcnow()
        user.password = PasswordEncryption.encrypt_password(user.password)
        user.user_group = self.user_group_service.get_default_user_group()

        try:
            self.user_dao.add(user)
        except DuplicateEntryException as exception:
            exception.error_code = ErrorCode.USER_LOGIN_ALREADY_EXISTS
            raise exception

        return user

    def update_by_dto(self, dto: dict):
        self.mapper.validate_dto(dto)

        user = self.find_by_id(dto.get("id"))

        if user != AuthenticationContext.get_current_user():
            raise PermissionException(ErrorCode.UPDATE_USER_PERMISSION, User.__name__, Actions.UPDATE)

        if not user:
            raise ObjectNotFoundException(User.__name__, {"id": dto.get("id")})

        user = self.mapper.to_object(dto, user)

        if dto.get("password"):
            user.password = PasswordEncryption.encrypt_password(dto.get("password"))

        self.user_dao.commit()
