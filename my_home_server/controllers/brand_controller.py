
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

import my_home_server.security.authentication_utils as authentication_utils
import my_home_server.controllers.errors_handler as errors_handler
from my_home_server.mappers.brand_mapper import BrandMapper
from my_home_server.services.brand_service import BrandService

controller = Blueprint("brand_controller", __name__, url_prefix="/api/brand")
errors_handler.fill_error_handlers_to_controller(controller)


@controller.route("/")
@jwt_required()
@authentication_utils.set_authentication_context
def get_all_brands(brand_service: BrandService, brand_mapper: BrandMapper):
    return jsonify(brand_mapper.from_list_to_dto(brand_service.find_all()))


@controller.route("<path:brand_id>")
@jwt_required()
@authentication_utils.set_authentication_context
def get_brand(brand_id: int, brand_service: BrandService, brand_mapper: BrandMapper):
    brand = brand_service.find_by_id(brand_id)
    return jsonify(brand_mapper.to_dto(brand))


@controller.route("/", methods=['POST'])
@jwt_required()
@authentication_utils.set_authentication_context
def create_brand(brand_service: BrandService, brand_mapper: BrandMapper):
    brand_dto = request.json
    brand = brand_service.create_from_dto(brand_dto)
    return jsonify(brand_mapper.to_dto(brand))


@controller.route("/", methods=['PUT'])
@jwt_required()
@authentication_utils.set_authentication_context
def update_brand(brand_service: BrandService, brand_mapper: BrandMapper):
    brand_dto = request.json
    brand = brand_service.update_from_dto(brand_dto)
    return jsonify(brand_mapper.to_dto(brand))


@controller.route("<path:brand_id>", methods=['DELETE'])
@jwt_required()
@authentication_utils.set_authentication_context
def delete_brand(brand_id: int, brand_service: BrandService):
    brand_service.delete_by_id(brand_id)
    return {}, 200
