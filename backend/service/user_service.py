import random
import string
from typing import List

import bcrypt
from bson import ObjectId
from pymongo.collection import Collection

from model.user import User
from service.mail_service import MailService


class UserService:
    def __init__(self, user_collection: Collection, mail_service: MailService, psw_salt):
        self.user_collection = user_collection
        self.mail_service = mail_service
        self.psw_salt = psw_salt

    def get_user_info_by_id(self, _id: str) -> User:
        return User.from_dict(self.user_collection.find_one({'_id': ObjectId(_id)}, {'password': 0}))

    def get_user_by_id(self, _id: str):
        return self.user_collection.find_one({'_id': ObjectId(_id)})

    def get_user_by_email(self, email: str):
        return self.user_collection.find_one({'email': email})

    def get_trainers_of_club(self, club_id: str) -> List[User]:
        return [User.from_dict(doc) for doc in self.user_collection.find({'club_ids': ObjectId(club_id), 'role': 2},
                                                                         {'password': 0})]

    def get_admins_of_club(self, club_id: str) -> List[User]:
        return [User.from_dict(doc) for doc in self.user_collection.find({'club_ids': ObjectId(club_id), 'role': 1},
                                                                         {'password': 0})]

    def add_club_to_user(self, user_id: str, club_id: str) -> None:
        user = User.from_dict(self.get_user_by_id(user_id))
        user_clubs = user.get_club_ids()
        if user_clubs is None:
            user_clubs = []
        user_clubs.append(ObjectId(club_id))
        self.user_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'club_ids': user_clubs}})

    def add_team_to_user(self, user_id: str, team_id: str) -> None:
        user = User.from_dict(self.get_user_by_id(user_id))
        user_teams = user.get_team_ids()
        if ObjectId(team_id) in user_teams:
            raise AttributeError("Team is already connected with provided team")
        user_teams.append(ObjectId(team_id))
        self.user_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'team_ids': user_teams}})

    def remove_team_from_user(self, user_id: str, team_id: str) -> None:
        user = User.from_dict(self.get_user_by_id(user_id))
        user_teams = user.get_team_ids()
        if user_teams is None or ObjectId(team_id) not in user_teams:
            raise AttributeError("User does not have specified team in it's team list")
        user_teams.remove(ObjectId(team_id))
        self.user_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'team_ids': user_teams}})

    def create_user(self, user: User) -> str:
        if user.get_image_url() is None:
            user.set_image_url('defaultavatar.png')
        if user.get_team_ids() is None:
            user.set_team_ids([])
        if user.get_club_ids() is None:
            user.set_club_ids([])
        original_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        hashed_psw = str(bcrypt.hashpw(original_password.encode('utf8'), self.psw_salt), 'utf8')
        user.set_password(hashed_psw)
        user_id = self.user_collection.insert_one(user.get_dict_value()).inserted_id
        user_mail = user.get_email()
        body = f'A new account has been created for the Athlete Monitor.\n\nUser: {user_mail}\nPassword: {original_password}'
        self.mail_service.send_mail(receiver=user_mail, subject='access code Athlete Monitor', content=body)
        return user_id

    def edit_user(self, user: User, password: str) -> None:
        if password is not None:
            hashed_psw = str(bcrypt.hashpw(password.encode('utf8'), self.psw_salt), 'utf8')
            user.set_password(hashed_psw)
        user_id = user.get_id()
        user.set_id(None)
        self.user_collection.update_one({'_id': ObjectId(user_id)}, {'$set': user.get_dict_value()})

    def delete_user(self, user_id: str) -> None:
        self.user_collection.delete_one({'_id': ObjectId(user_id)})

    def delete_common_users_with_club_id(self, club_id: str) -> None:
        self.user_collection.delete_many({'$and': [{'club_ids': ObjectId(club_id)}, {'role': {'$ne': 0}}]})

    def remove_club_from_users(self, club_id: str) -> None:
        self.user_collection.update_many({}, {'$pull': {'club_ids': ObjectId(club_id)}})

    def remove_team_from_users(self, team_id: str) -> None:
        self.user_collection.update_many({}, {'$pull': {'team_ids': ObjectId(team_id)}})

    def reset_user_password(self, user_id: str) -> None:
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        hashed_password = str(bcrypt.hashpw(new_password.encode('utf8'), self.psw_salt), 'utf8')
        self.user_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'password': hashed_password}})
        user = self.get_user_info_by_id(user_id)
        user_mail = user.get_email()
        body = f'Your password has been reset for the Athlete Monitor.\n\nUser: {user_mail}\nPassword: {new_password}'
        self.mail_service.send_mail(receiver=user_mail, subject='password reset Athlete Monitor', content=body)
