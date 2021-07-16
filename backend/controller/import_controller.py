from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app import app, connection_service, import_process_service
from import_module.service.import_configuration_service import ImportConfigurationService
from utils.function_wrappers import club_user_permission_required, single_club_per_user, error_handler

import_configuration_service = ImportConfigurationService(connection_service)

@app.route('/api/import/configuration/all', methods=['GET'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def get_configuration():
    return jsonify(
        list(
            map(lambda x: x.get_dict_value(), import_configuration_service.get_all_club_configurations()))), 200


@app.route('/api/import', methods=['POST'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def import_files():
    import_process_service.import_data(request.form.get('configuration_id'), request.files.getlist('files'))
    return '', 200
