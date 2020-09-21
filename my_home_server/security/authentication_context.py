from my_home_server.models.user import User
from my_home_server.security.authentication_data import AuthenticationData
from my_home_server.services.user_service import UserService


class AuthenticationContext(object):
    __authentication_context = None

    current_user: User
    authentication_data: AuthenticationData

    @staticmethod
    def init_context(authentication_data: AuthenticationData, user_service: UserService):
        AuthenticationContext.__authentication_context = AuthenticationContext()

        AuthenticationContext.__authentication_context.authentication_data = authentication_data
        AuthenticationContext.__authentication_context.current_user = user_service.find_by_id(
            authentication_data.user_id)

    @staticmethod
    def get_context():
        return AuthenticationContext.__authentication_context

    @staticmethod
    def get_current_user() -> User:
        return AuthenticationContext.__authentication_context.current_user
