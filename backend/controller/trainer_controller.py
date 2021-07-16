from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app import app, club_admin_permission_required, single_club_per_user, error_handler, file_upload_service, \
    user_service, current_user, team_service
from model.user import User


@app.route('/api/trainer', methods=['POST'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def create_trainer():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = request.host_url + 'api/image/defaultavatar.png'
    user = User(role=2, email=request.form.get('email'), image_url=file_url, club_ids=[ObjectId(current_user['club_ids'][0])])
    return {'created': user_service.create_user(user)}, 201


@app.route('/api/-', methods=['DELETE'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def delete_trainer():
    user_id = request.args.get('user_id')
    team_service.delete_trainer(user_id)
    return {'deleted': user_id}, 200


@app.route('/api/trainer/all', methods=['GET'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def get_all_trainers():
    club_id = current_user['club_ids'][0]
    return jsonify(list(map(lambda x: x.get_dict_value(), user_service.get_trainers_of_club(club_id)))), 200


@app.route('/api/trainer/reset', methods=['PUT'])
@jwt_required()
@club_admin_permission_required
@error_handler
def reset_trainer_password():
    user_id = request.args.get('user_id')
    user_service.reset_user_password(user_id)
    return {'updated': user_id}, 200


@app.route('/api/trainer/connect', methods=['PUT'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def connect_trainer():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')
    team_service.connect_trainer(user_id, team_id)
    return {'msg': 'success'}, 200


@app.route('/api/trainer/disconnect', methods=['PUT'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def disconnect_trainer():
    user_id = request.args.get('user_id')
    team_id = request.args.get('team_id')
    team_service.disconnect_trainer(user_id, team_id)
    return {'msg': 'success'}, 200

