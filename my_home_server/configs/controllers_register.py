from flask import Flask

import my_home_server.controllers.user_controller as user_controller
import my_home_server.controllers.brand_controller as brand_controller
import my_home_server.controllers.product_type_controller as product_type_controller
import my_home_server.controllers.product_controller as product_controller
import my_home_server.controllers.purchase_list_controller as purchase_list_controller
import my_home_server.controllers.purchase_controller as purchase_controller


def register_controllers(app: Flask):
    app.register_blueprint(user_controller.controller)
    app.register_blueprint(brand_controller.controller)
    app.register_blueprint(product_type_controller.controller)
    app.register_blueprint(product_controller.controller)
    app.register_blueprint(purchase_list_controller.controller)
    app.register_blueprint(purchase_controller.controller)
