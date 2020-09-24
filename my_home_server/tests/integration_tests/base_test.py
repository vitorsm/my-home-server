import os

from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask_injector import FlaskInjector
from injector import Injector
from flask_testing import TestCase

from my_home_server.configs.dependencies_injector import AppModule
from my_home_server.models.base_models import Base
from my_home_server.models.user import User
from my_home_server.models.user_group import UserGroup
from my_home_server.security import authentication_utils
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.security.password_encryption import PasswordEncryption

import my_home_server.configs.controllers_register as controllers_register
from my_home_server.services.user_service import UserService


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    ENCRYPT_SECRET_KEY = "tests"

    app: Flask
    db: SQLAlchemy

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = self.ENCRYPT_SECRET_KEY
        self.app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"

        controllers_register.register_controllers(self.app)

        def authenticate(login: str, password: str):
            user_service = self.dependency_injector.get(UserService)
            return authentication_utils.authenticate(login, password, user_service)

        def identity(payload: dict):
            user_service = self.dependency_injector.get(UserService)
            return authentication_utils.identity(payload, user_service)

        self.db = SQLAlchemy(self.app, session_options={"autoflush": False})
        jwt = JWT(self.app, authenticate, identity)

        self.dependency_injector = Injector([AppModule(self.app, self.db)])
        FlaskInjector(app=self.app, injector=self.dependency_injector)

        return self.app

    def setUp(self):
        Base.metadata.create_all(self.db.get_engine())
        default_user = BaseTest.__get_default_user()

        self.db.session.add(default_user.user_group)
        self.db.session.add(default_user)
        self.initial_load()
        self.db.session.commit()

        AuthenticationContext.init_context(default_user)

    def initial_load(self):
        # /home/vitor/git/my-home-server/my_home_server//my_home_server/tests/resources/initial_load.sql
        file_path = BaseTest.get_current_dir() + "tests/resources/initial_load.sql"
        file = open(file_path)
        for query in file.read().split(";"):
            if query.strip():
                self.db.session.execute(query.strip())
        file.close()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    @staticmethod
    def __get_default_user_group():
        user_group = UserGroup()
        user_group.id = 1
        user_group.name = "Default"

        return user_group

    @staticmethod
    def __get_default_user():
        user = User()
        user.id = 1
        user.name = "Default"
        user.login = "default"
        user.password = PasswordEncryption.encrypt_password("default")
        user.user_group = BaseTest.__get_default_user_group()

        return user

    @staticmethod
    def get_current_dir():
        path = os.getcwd()
        if "my_home_server/tests" in path:
            index = path.index("my_home_server/tests")
            path = path[:index]

        return path + "/" if path.endswith("/my_home_server") else path + "/my_home_server/"
