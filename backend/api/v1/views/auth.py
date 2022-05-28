from models import User
from flask import Blueprint, request, jsonify, abort
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    unset_jwt_cookies, current_user, jwt_required
)
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    username = request.get_json().get('username', None)
    password = request.get_json().get('password', None)
    user = User.query.filter(User.username == username).one()
    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            response = jsonify(
                {"msg": "login successful", "access_token": access_token})
            set_access_cookies(response, access_token)
            return response
        else:
            return jsonify(error='Incorrect password')
    else:
        return jsonify(error='User doesn\'t exist')


@bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@bp.route('/whoami')
@jwt_required()
def whoami():
    return jsonify(current_user.to_dict())


def admin_only(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.role.name != "admin":
            abort(400, description="Admin only")
        return view(**kwargs)
    return wrapped_view
