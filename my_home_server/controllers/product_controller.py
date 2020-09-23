
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

import my_home_server.security.authentication_utils as authentication_utils
import my_home_server.controllers.errors_handler as errors_handler
from my_home_server.mappers.product_mapper import ProductMapper
from my_home_server.services.product_service import ProductService

controller = Blueprint("product_controller", __name__, url_prefix="/api/product")
errors_handler.fill_error_handlers_to_controller(controller)


@controller.route("/")
@jwt_required()
@authentication_utils.set_authentication_context
def get_all_products(product_service: ProductService, product_mapper: ProductMapper):
    return jsonify(product_mapper.from_list_to_dto(product_service.find_all()))


@controller.route("<path:product_id>")
@jwt_required()
@authentication_utils.set_authentication_context
def get_product(product_id: int, product_service: ProductService, product_mapper: ProductMapper):
    product = product_service.find_by_id(product_id)
    return jsonify(product_mapper.to_dto(product))


@controller.route("/", methods=['POST'])
@jwt_required()
@authentication_utils.set_authentication_context
def create_product(product_service: ProductService, product_mapper: ProductMapper):
    product_dto = request.json
    product = product_service.create_from_dto(product_dto)
    return jsonify(product_mapper.to_dto(product))


@controller.route("/", methods=['PUT'])
@jwt_required()
@authentication_utils.set_authentication_context
def update_product(product_service: ProductService, product_mapper: ProductMapper):
    product_dto = request.json
    product = product_service.update_from_dto(product_dto)
    return jsonify(product_mapper.to_dto(product))


@controller.route("<path:product_id>", methods=['DELETE'])
@jwt_required()
@authentication_utils.set_authentication_context
def delete_product(product_id: int, product_service: ProductService):
    product_service.delete_by_id(product_id)
    return {}, 200
