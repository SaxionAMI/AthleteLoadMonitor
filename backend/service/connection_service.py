from bson import ObjectId
from flask_pymongo import PyMongo


class ConnectionService:
    def __init__(self, club_collection, app):
        self.club_collection = club_collection
        self.app = app
        self.connection_map = {}
        self.update_connection_map()

    def get_connection_by_club_id(self, club_id: ObjectId) -> PyMongo:
        return self.connection_map[club_id]

    def update_connection_map(self) -> None:
        self.connection_map = {}
        for c in self.club_collection.find():
            self.connection_map[c['_id']] = PyMongo(self.app, uri=c['database_url'])

    def drop_db(self, club_id: ObjectId) -> None:
        self.get_connection_by_club_id(club_id=club_id).db.drop_collection('player')
        self.get_connection_by_club_id(club_id=club_id).db.drop_collection('team')
        self.get_connection_by_club_id(club_id=club_id).db.drop_collection('training')

