from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app import app, club_user_permission_required, single_club_per_user, error_handler, file_upload_service, \
    team_service, club_admin_permission_required
from model.team import Team


@app.route('/api/team', methods=['POST'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def add_team():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = request.host_url + 'api/image/defaultteam.png'
    team = Team(image_url=file_url, name=request.form['name'], player_ids=[])
    team_id = team_service.add(team)
    return {'created': team_id}, 201


@app.route('/api/team', methods=['DELETE'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def delete_team():
    team_id = request.args.get('team_id')
    team_service.delete(team_id)
    return {'deleted': team_id}, 200


@app.route('/api/team', methods=['PUT'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def update_team():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = None
    team = Team(_id=request.form['_id'], name=request.form['name'], image_url=file_url)
    team_service.edit(team)
    return {'updated': request.form['_id']}, 200


@app.route('/api/team/all', methods=['GET'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def get_all_teams():
    return jsonify(list(map(lambda x: x.get_dict_value(), team_service.get_all()))), 200
