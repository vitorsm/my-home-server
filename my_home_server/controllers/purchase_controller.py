
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

import my_home_server.security.authentication_utils as authentication_utils
import my_home_server.controllers.errors_handler as errors_handler
from my_home_server.mappers.purchase_mapper import PurchaseMapper
from my_home_server.services.purchase_service import PurchaseService

controller = Blueprint("purchase_controller", __name__, url_prefix="/api/purchase")
errors_handler.fill_error_handlers_to_controller(controller)


@controller.route("/")
@jwt_required()
@authentication_utils.set_authentication_context
def get_all_purchases(purchase_service: PurchaseService, purchase_mapper: PurchaseMapper):
    return jsonify(purchase_mapper.from_list_to_dto(purchase_service.find_all()))


@controller.route("<path:purchase_id>")
@jwt_required()
@authentication_utils.set_authentication_context
def get_purchase(purchase_id: int, purchase_service: PurchaseService, purchase_mapper: PurchaseMapper):
    purchase = purchase_service.find_by_id(purchase_id)
    return jsonify(purchase_mapper.to_dto(purchase))


@controller.route("/", methods=['POST'])
@jwt_required()
@authentication_utils.set_authentication_context
def create_purchase(purchase_service: PurchaseService, purchase_mapper: PurchaseMapper):
    purchase_dto = request.json
    purchase = purchase_service.create_from_dto(purchase_dto)
    return jsonify(purchase_mapper.to_dto(purchase))


@controller.route("/", methods=['PUT'])
@jwt_required()
@authentication_utils.set_authentication_context
def update_purchase(purchase_service: PurchaseService, purchase_mapper: PurchaseMapper):
    purchase_dto = request.json
    purchase = purchase_service.update_from_dto(purchase_dto)
    return jsonify(purchase_mapper.to_dto(purchase))


@controller.route("<path:purchase_id>", methods=['DELETE'])
@jwt_required()
@authentication_utils.set_authentication_context
def delete_purchase(purchase_id: int, purchase_service: PurchaseService):
    purchase_service.delete_by_id(purchase_id)
    return {}, 200
