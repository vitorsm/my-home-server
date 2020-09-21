import inspect

from injector import Module, singleton
from flask_sqlalchemy import SQLAlchemy

from my_home_server.dao.brand_dao import BrandDAO
from my_home_server.dao.product_dao import ProductDAO
from my_home_server.dao.product_type_dao import ProductTypeDAO
from my_home_server.dao.purchase_dao import PurchaseDAO
from my_home_server.dao.purchase_list_dao import PurchaseListDAO
from my_home_server.dao.user_dao import UserDAO
from my_home_server.dao.user_group_dao import UserGroupDAO
from my_home_server.services.brand_service import BrandService
from my_home_server.services.product_service import ProductService
from my_home_server.services.product_type_service import ProductTypeService
from my_home_server.services.purchase_list_service import PurchaseListService
from my_home_server.services.user_group_service import UserGroupService
from my_home_server.services.user_service import UserService


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    @staticmethod
    def get_dependencies_instances(db) -> list:
        return [
            BrandDAO(db),
            ProductDAO(db),
            ProductTypeDAO(db),
            PurchaseDAO(db),
            PurchaseListDAO(db),
            UserDAO(db),
            UserGroupDAO(db),
            BrandService(),
            ProductService(),
            ProductTypeService(),
            PurchaseListService(),
            UserGroupService(),
            UserService()
        ]

    def configure(self, binder):
        db = SQLAlchemy(self.app)

        instances = self.get_dependencies_instances(db)

        for instance in instances:
            binder.bind(type(instance), to=instance, scope=singleton)
