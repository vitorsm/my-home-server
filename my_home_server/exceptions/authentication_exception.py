

class AuthenticationException(Exception):
    def __init__(self, login: str):
        super().__init__(f"Authentication failed for {login}")
        self.login = login
