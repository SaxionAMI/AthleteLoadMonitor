from typing import List

from bson import ObjectId
from flask_jwt_extended import current_user
from pymongo.collection import Collection

from import_module.model.file_import_configuration import FileImportConfiguration
from service.connection_service import ConnectionService


class ImportConfigurationService:
    def __init__(self, connection_service: ConnectionService):
        self.connection_service = connection_service

    def get_all_club_configurations(self) -> List[FileImportConfiguration]:
        return [FileImportConfiguration.from_dict(doc) for doc in self.__get_connection().find()]

    def __get_connection(self) -> Collection:
        return self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0]))\
            .db.file_import_configuration
