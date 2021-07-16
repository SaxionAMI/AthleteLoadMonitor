from app import app, connection_service
from flask import jsonify, request
from flask_jwt_extended import jwt_required

from service.player_training_managment_service import PlayerTrainingManagementService
from utils.function_wrappers import single_club_per_user, error_handler, club_admin_permission_required

player_training_management_service = PlayerTrainingManagementService(connection_service)


@app.route('/api/training/management/unmapped-player/all', methods=['GET'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def get_unmapped_player_names():
    return jsonify(player_training_management_service.get_unmapped_players_from_trainings()), 200


@app.route('/api/training/management/unmapped-player', methods=['DELETE'])
@jwt_required()
@club_admin_permission_required
@single_club_per_user
@error_handler
def delete_unmapped_players():
    player_training_management_service.delete_unmapped_player(request.args.get('player_name'))
    return {}, 204
