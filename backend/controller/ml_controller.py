from flask import request
from flask_jwt_extended import jwt_required

from app import app, connection_service
from ml_module.service.ml_training_service import MLTrainingService
from utils.function_wrappers import club_user_permission_required, single_club_per_user, error_handler

ml_training_service = MLTrainingService(connection_service)

@app.route('/api/ml/train_new', methods=['POST'])
@jwt_required()
@club_user_permission_required
@single_club_per_user
@error_handler
def train_new_model():
    start_date = request.args.get('start_date', type=int)
    end_date = request.args.get('end_date', type=int)
    ml_training_service.train_new_model(start_date, end_date)
    return '', 200
