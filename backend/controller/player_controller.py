from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app import app, club_user_permission_required, single_club_per_user, error_handler, file_upload_service, \
    player_service, team_service, training_service
from model.player import Player


@app.route('/api/player', methods=['POST'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def create_player():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = request.host_url + 'api/image/defaultavatar.png'
    player = Player(name=request.form['name'], position=request.form['position'],
                    image_url=file_url, name_variations=[request.form['name']])
    player_id = player_service.add(player)
    team_service.add_player(request.form['team_id'], player_id)
    return {'created': player_id}, 201


@app.route('/api/player', methods=['DELETE'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def delete_player():
    player_id = request.args.get('player_id')
    player_service.delete(player_id)
    return {'deleted': player_id}, 200


@app.route('/api/player', methods=['PUT'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def update_player():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = request.host_url + 'api/image/defaultteam.png'
    player = Player(_id=request.form['_id'], name=request.form['name'],
                    position=request.form['position'], image_url=file_url)
    player_service.edit(player)
    return {'updated': request.form['_id']}, 200


@app.route('/api/player/all', methods=['GET'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def get_all_players():
    return jsonify(list(map(lambda x: x.get_dict_value(), player_service.get_all()))), 200


@app.route('/api/player/team/all', methods=['GET'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def get_all_team_players():
    team_id = request.args.get('team_id')
    return jsonify(list(map(lambda x: x.get_dict_value(), player_service.get_team_all(team_id)))), 200


@app.route('/api/player/changeTeamPlayer', methods=['PUT'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def change_player_team():
    player_service.change_team(request.form['old_team_id'], request.form['new_team_id'], request.form['player_id'])
    return {'success': request.form['player_id']}, 200


@app.route('/api/player/add-name-variation', methods=['PUT'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def add_name_variation_to_player():
    player_service.add_name_variation(request.json['player_id'], request.json['name'])
    return {}, 200


@app.route('/api/player/trainings', methods=['GET'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def get_player_trainings():
    player_id = request.args.get('player_id')
    return jsonify(training_service.get_player_trainings(player_id)), 200


@app.route('/api/player/averages', methods=['GET'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def get_player_averages():
    player_id = request.args.get('player_id')
    return jsonify(training_service.get_player_training_averages(player_id)), 200


@app.route('/api/ml/configuration', methods=['GET'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def get_ml_configuration():
    return jsonify(training_service.get_configuration()), 200
