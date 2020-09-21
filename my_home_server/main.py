from flask import Flask
from flask_injector import FlaskInjector
from injector import Injector

from my_home_server.configs import config
from my_home_server.configs.dependencies_injector import AppModule

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['BAD_FILES_FOLDER'] = 'bad_files'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dependency_injector = Injector([AppModule(app)])


def auto_wired(function):
    def function_wrapper():
        obj = function()
        annotations = obj.__annotations__

        for attribute in annotations:
            pass

    return function_wrapper


if __name__ == "__main__":

    FlaskInjector(app=app, injector=dependency_injector)
    app.run(host='0.0.0.0', port=config.HOST_PORT)
