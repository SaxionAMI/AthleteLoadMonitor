from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from app import app, error_handler
from service.menu_service import MenuService

menu_service = MenuService()


@app.route("/api/menu", methods=["GET"])
@jwt_required()
@error_handler
def get_menu():
    return jsonify(menu_service.get_menu_by_role(current_user['role'])), 200
