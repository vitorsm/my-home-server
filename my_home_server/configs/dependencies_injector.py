from flask import Flask
from injector import Module, singleton, Binder
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
from my_home_server.services.purchase_service import PurchaseService
from my_home_server.services.user_group_service import UserGroupService
from my_home_server.services.user_service import UserService


class AppModule(Module):

    def __init__(self, app: Flask, db: SQLAlchemy = None):
        self.app = app
        self.db = db

    def configure(self, binder: Binder):
        if not self.db:
            self.db = SQLAlchemy(self.app, session_options={"autoflush": False})

        dependencies = list()

        brand_dao = BrandDAO(self.db)
        dependencies.append(brand_dao)

        product_dao = ProductDAO(self.db)
        dependencies.append(product_dao)
        product_type_dao = ProductTypeDAO(self.db)
        dependencies.append(product_type_dao)
        purchase_dao = PurchaseDAO(self.db)
        dependencies.append(purchase_dao)
        purchase_list_dao = PurchaseListDAO(self.db)
        dependencies.append(purchase_list_dao)
        user_dao = UserDAO(self.db)
        dependencies.append(user_dao)
        user_group_dao = UserGroupDAO(self.db)
        dependencies.append(user_group_dao)

        brand_service = BrandService(brand_dao)
        dependencies.append(brand_service)
        product_type_service = ProductTypeService(product_type_dao)
        dependencies.append(product_type_service)
        product_service = ProductService(product_dao, brand_service, product_type_service)
        dependencies.append(product_service)
        purchase_list_service = PurchaseListService(purchase_list_dao, product_service)
        dependencies.append(purchase_list_service)
        user_group_service = UserGroupService(user_group_dao)
        dependencies.append(user_group_service)
        user_service = UserService(user_dao, user_group_service)
        dependencies.append(user_service)
        purchase_service = PurchaseService(purchase_dao, purchase_list_service, product_service)
        dependencies.append(purchase_service)

        for instance in dependencies:
            binder.bind(type(instance), to=instance, scope=singleton)
