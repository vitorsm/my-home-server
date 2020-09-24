from datetime import timedelta

from flask import Flask
from flask_jwt import JWT

from flask_injector import FlaskInjector
from injector import Injector

from my_home_server.configs import config
from my_home_server.configs.dependencies_injector import AppModule

import my_home_server.security.authentication_utils as authentication_utils
import my_home_server.configs.controllers_register as controllers_register

from my_home_server.services.user_service import UserService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.ENCRYPT_SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=config.HOURS_TO_EXPIRATION_TOKEN)


def authenticate(login: str, password: str):
    user_service = dependency_injector.get(UserService)
    return authentication_utils.authenticate(login, password, user_service)


def identity(payload: dict):
    user_service = dependency_injector.get(UserService)
    return authentication_utils.identity(payload, user_service)


jwt = JWT(app, authenticate, identity)

dependency_injector = Injector([AppModule(app)])

controllers_register.register_controllers(app)


if __name__ == "__main__":

    FlaskInjector(app=app, injector=dependency_injector)
    app.run(host='0.0.0.0', port=config.HOST_PORT)
