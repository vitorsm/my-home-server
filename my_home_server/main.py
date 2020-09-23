from datetime import timedelta

from flask import Flask
from flask_jwt import JWT

from flask_injector import FlaskInjector
from injector import Injector

from my_home_server.configs import config
from my_home_server.configs.dependencies_injector import AppModule

import my_home_server.security.authentication_utils as authentication_utils

import my_home_server.controllers.user_controller as user_controller
import my_home_server.controllers.brand_controller as brand_controller
import my_home_server.controllers.product_type_controller as product_type_controller
import my_home_server.controllers.product_controller as product_controller
import my_home_server.controllers.purchase_list_controller as purchase_list_controller
import my_home_server.controllers.purchase_controller as purchase_controller

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

app.register_blueprint(user_controller.controller)
app.register_blueprint(brand_controller.controller)
app.register_blueprint(product_type_controller.controller)
app.register_blueprint(product_controller.controller)
app.register_blueprint(purchase_list_controller.controller)
app.register_blueprint(purchase_controller.controller)


if __name__ == "__main__":

    FlaskInjector(app=app, injector=dependency_injector)
    app.run(host='0.0.0.0', port=config.HOST_PORT)
