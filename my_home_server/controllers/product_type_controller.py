
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

import my_home_server.security.authentication_utils as authentication_utils
import my_home_server.controllers.errors_handler as errors_handler
from my_home_server.mappers.product_type_mapper import ProductTypeMapper
from my_home_server.services.product_type_service import ProductTypeService

controller = Blueprint("product_type_controller", __name__, url_prefix="/api/product-type")
errors_handler.fill_error_handlers_to_controller(controller)


@controller.route("/")
@jwt_required()
@authentication_utils.set_authentication_context
def get_all_product_types(product_type_service: ProductTypeService, product_type_mapper: ProductTypeMapper):
    return jsonify(product_type_mapper.from_list_to_dto(product_type_service.find_all()))


@controller.route("<path:product_type_id>")
@jwt_required()
@authentication_utils.set_authentication_context
def get_product_type(product_type_id: int, product_type_service: ProductTypeService,
                     product_type_mapper: ProductTypeMapper):
    product_type = product_type_service.find_by_id(product_type_id)
    return jsonify(product_type_mapper.to_dto(product_type))


@controller.route("/", methods=['POST'])
@jwt_required()
@authentication_utils.set_authentication_context
def create_product_type(product_type_service: ProductTypeService, product_type_mapper: ProductTypeMapper):
    product_type_dto = request.json
    product_type = product_type_service.create_from_dto(product_type_dto)
    return jsonify(product_type_mapper.to_dto(product_type))


@controller.route("/", methods=['PUT'])
@jwt_required()
@authentication_utils.set_authentication_context
def update_product_type(product_type_service: ProductTypeService, product_type_mapper: ProductTypeMapper):
    product_type_dto = request.json
    product_type = product_type_service.update_from_dto(product_type_dto)
    return jsonify(product_type_mapper.to_dto(product_type))


@controller.route("<path:product_type_id>", methods=['DELETE'])
@jwt_required()
@authentication_utils.set_authentication_context
def delete_product_type(product_type_id: int, product_type_service: ProductTypeService):
    product_type_service.delete_by_id(product_type_id)
    return {}, 200

