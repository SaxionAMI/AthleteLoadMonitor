import datetime
import os
import tempfile

import bcrypt
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from flask_pymongo import PyMongo, ASCENDING

from service.club_service import ClubService
from service.connection_service import ConnectionService
from service.file_upload_service import FileUploadService
from service.mail_service import MailService
from service.player_service import PlayerService
from service.team_service import TeamService
from service.training_service import TrainingService
from service.user_service import UserService
from import_module.service.import_process_service import ImportProcessService
from utils.function_wrappers import *
from utils.mongo_json_encoder import MongoJSONEncoder, ObjectIdConverter

from waitress import serve

temp_dir = tempfile.TemporaryDirectory()

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = os.path.join('uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["JWT_SECRET_KEY"] = "super-secret"  # todo Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=8)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'athletemailer'  # TODO configure SMTP account
app.config['MAIL_PASSWORD'] = '89XFv8zvWSPp4mfwab'  # TODO configure SMTP account
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.json_encoder = MongoJSONEncoder
app.url_map.converters['objectId'] = ObjectIdConverter

MONGO_URL = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'general'
salt = bcrypt.gensalt(10)

jwt = JWTManager(app)
general_mongo = PyMongo(app, uri=MONGO_URL + MONGO_DB_NAME)
DEBUG = True

mail_service = MailService(app)
user_service = UserService(general_mongo.db.user, mail_service, salt)
connection_service = ConnectionService(general_mongo.db.club, app)
file_upload_service = FileUploadService(app)
club_service = ClubService(general_mongo.db.club, MONGO_URL, user_service, connection_service)
team_service = TeamService(connection_service, user_service)
import_process_service = ImportProcessService(connection_service)
player_service = PlayerService(connection_service, team_service, import_process_service)
training_service = TrainingService(connection_service)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user['_id'])


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return user_service.get_user_by_id(identity)


@app.route("/api/auth/login", methods=["POST"])
@error_handler
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = user_service.get_user_by_email(email)
    if not user or not bcrypt.checkpw(password.encode('utf8'), user['password'].encode('utf8')):
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@app.route("/api/auth/user", methods=["GET"])
@jwt_required()
@error_handler
def get_user():
    user = user_service.get_user_info_by_id(current_user['_id'])
    return jsonify(user.get_dict_value()), 200


@app.route('/api/user', methods=['PUT'])
@jwt_required()
@error_handler
def edit_user():
    file_name = file_upload_service.upload_image(request.files.get('image'))
    if file_name is not None:
        file_url = request.host_url + 'api/image/' + file_name
    else:
        file_url = None
    user = User(_id=request.form.get('user_id'), image_url=file_url)
    user_service.edit_user(user, request.form.get('password'))
    return {'updated': request.form.get('user_id')}, 200


from controller.image_controller import *
from controller.menu_controller import *
from controller.club_controller import *
from controller.player_controller import *
from controller.team_controller import *
from controller.trainer_controller import *
from controller.import_controller import *
from controller.player_training_management_controller import *
from controller.ml_controller import *


if __name__ == '__main__':
    with app.app_context():
        general_mongo.db.club.create_index([("name", ASCENDING), ("database_url", ASCENDING)], unique=True)
        general_mongo.db.user.create_index([("email", ASCENDING)], unique=True)

    serve(app, host="0.0.0.0", port=5000)
    # app.run()
