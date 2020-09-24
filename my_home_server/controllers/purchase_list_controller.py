
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

import my_home_server.security.authentication_utils as authentication_utils
import my_home_server.controllers.errors_handler as errors_handler
from my_home_server.mappers.purchase_list_mapper import PurchaseListMapper
from my_home_server.services.purchase_list_service import PurchaseListService

controller = Blueprint("purchase_list_controller", __name__, url_prefix="/api/purchase-list")
errors_handler.fill_error_handlers_to_controller(controller)


@controller.route("/")
@jwt_required()
@authentication_utils.set_authentication_context
def get_all_purchase_lists(purchase_list_service: PurchaseListService, purchase_list_mapper: PurchaseListMapper):
    return jsonify(purchase_list_mapper.from_list_to_dto(purchase_list_service.find_all()))


@controller.route("<path:purchase_list_id>")
@jwt_required()
@authentication_utils.set_authentication_context
def get_purchase_list(purchase_list_id: str, purchase_list_service: PurchaseListService,
                      purchase_list_mapper: PurchaseListMapper):
    purchase_list = purchase_list_service.find_by_id(int(purchase_list_id))
    return jsonify(purchase_list_mapper.to_dto(purchase_list))


@controller.route("/", methods=['POST'])
@jwt_required()
@authentication_utils.set_authentication_context
def create_purchase_list(purchase_list_service: PurchaseListService, purchase_list_mapper: PurchaseListMapper):
    purchase_list_dto = request.json
    purchase_list = purchase_list_service.create_from_dto(purchase_list_dto)
    return jsonify(purchase_list_mapper.to_dto(purchase_list))


@controller.route("/", methods=['PUT'])
@jwt_required()
@authentication_utils.set_authentication_context
def update_purchase_list(purchase_list_service: PurchaseListService, purchase_list_mapper: PurchaseListMapper):
    purchase_list_dto = request.json
    purchase_list = purchase_list_service.update_from_dto(purchase_list_dto)
    return jsonify(purchase_list_mapper.to_dto(purchase_list))


@controller.route("<path:purchase_list_id>", methods=['DELETE'])
@jwt_required()
@authentication_utils.set_authentication_context
def delete_purchase_list(purchase_list_id: str, purchase_list_service: PurchaseListService):
    purchase_list_service.delete_by_id(int(purchase_list_id))
    return {}, 200
