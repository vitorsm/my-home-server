from my_home_server.models.user import User


class AuthenticationContext(object):
    __authentication_context = None

    @staticmethod
    def init_context(user: User):
        AuthenticationContext.__authentication_context = AuthenticationContext()

        AuthenticationContext.__authentication_context.current_user = user

    @staticmethod
    def get_current_user() -> User:
        return AuthenticationContext.__authentication_context.current_user
