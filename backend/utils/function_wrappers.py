import traceback
from functools import wraps

from flask_jwt_extended import current_user
from pymongo.errors import DuplicateKeyError

from constants.roles import Role


def admin_permission_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user['role'] == Role.ADMIN.value[0]:
            return {'msg': 'Unauthorized. Admin permissions required'}, 401
        return func(*args, **kwargs)

    return decorated_function


def club_admin_permission_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user['role'] == Role.CLUB_ADMIN.value[0]:
            return {'msg': 'Unauthorized. Club admin permissions required'}, 401
        return func(*args, **kwargs)

    return decorated_function


def club_user_permission_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user['role'] == Role.ADMIN.value[0]:
            return {'msg': 'Unauthorized. Club user permissions required'}, 401
        return func(*args, **kwargs)

    return decorated_function


def single_club_per_user(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not len(current_user['club_ids']) == 1:
            return {
                       'msg': 'System error. user is associated with more then one club. contact system administrator'}, 500
        return func(*args, **kwargs)

    return decorated_function


def error_handler(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DuplicateKeyError:
            traceback.print_exc()
            return {'msg': 'Duplicate key error.'}, 400
        except AttributeError as e:
            traceback.print_exc()
            return {'msg': str(e)}, 400
        except FileNotFoundError as e:
            traceback.print_exc()
            return {'msg': 'Specified file not found'}, 404
        except Exception:
            traceback.print_exc()
            return {'msg': 'Internal server error'}, 500

    return decorated_function
