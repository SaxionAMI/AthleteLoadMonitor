from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app import app, admin_permission_required, error_handler, file_upload_service, club_service, user_service
from model.club import Club
from model.user import User


@app.route('/api/club', methods=['POST'])
@jwt_required()
@admin_permission_required
@error_handler
def add_club():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = request.host_url + 'api/image/defaultteam.png'
    club = Club(name=request.form['name'], image_url=file_url)
    return {'created': club_service.add(club)}, 201


@app.route('/api/club', methods=['DELETE'])
@jwt_required()
@admin_permission_required
@error_handler
def delete_club():
    club_id = request.args.get('club_id')
    club_service.delete(club_id)
    return {'deleted': club_id}, 200


@app.route('/api/club/', methods=['PUT'])
@jwt_required()
@admin_permission_required
@error_handler
def update_club():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = None
    club = Club(_id=request.form['_id'], name=request.form['name'], image_url=file_url)
    club_service.edit(club)
    return {'updated': request.form['_id']}, 200


@app.route('/api/club/all', methods=['GET'])
@jwt_required()
@admin_permission_required
@error_handler
def get_all_clubs():
    return jsonify(list(map(lambda x: x.get_dict_value(), club_service.get_all()))), 200


@app.route('/api/club/admin', methods=['POST'])
@jwt_required()
@admin_permission_required
@error_handler
def create_club_admin():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = request.host_url + 'api/image/defaultavatar.png'
    user = User(role=1, email=request.form['email'], image_url=file_url, club_ids=[ObjectId(request.form['club_id'])])
    user_id = user_service.create_user(user)
    return {'created': user_id}, 201


@app.route('/api/club/admin', methods=['DELETE'])
@jwt_required()
@admin_permission_required
@error_handler
def delete_club_admin():
    user_id = request.args.get('user_id')
    user_service.delete_user(user_id)
    return {'deleted': user_id}, 201


@app.route('/api/club/admin/all', methods=['GET'])
@jwt_required()
@admin_permission_required
@error_handler
def get_all_admins_of_club():
    club_id = request.args.get('club_id')
    return jsonify(list(map(lambda x: x.get_dict_value(), user_service.get_admins_of_club(club_id)))), 200


@app.route('/api/club/admin/reset', methods=['PUT'])
@jwt_required()
@admin_permission_required
@error_handler
def reset_club_admin_password():
    user_id = request.args.get('user_id')
    user_service.reset_user_password(user_id)
    return {'updated': user_id}, 200
