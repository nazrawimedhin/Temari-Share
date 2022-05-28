from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, current_user
from models import User, Resource, Role, Department
from .auth import admin_only

from app import db


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@jwt_required()
@admin_only
def get_all_user():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'username' not in data:
        return {'error': 'username is required'}, 400
    if 'email' not in data:
        return {'error': 'email is required'}, 400
    if 'password' not in data:
        return {'error': 'password is required'}, 400
    user_role = Role.query.filter(Role.name == 'user').one()
    user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        role_id=user_role.id
    )
    db.session.add(user)
    return user.to_dict()


@bp.route("/<int:id>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def get_user(id):
    user = User.query.filter(User.id == id).first_or_404()
    if request.method == 'PUT':
        args = request.get_json()
        user.update(**args)
    elif request.method == 'DELETE':
        db.session.delete(user)
    return user.to_dict()


@bp.route("/<int:id>/resources", methods=['GET', 'POST'])
@jwt_required()
def get_resources_by_user(id):
    if request.method == 'POST':
        data = request.get_json()
        if 'title' not in data:
            return {'error': 'title is required'}, 400
        if 'data' not in data:
            return {'error': 'data is required'}, 400
        if 'dept' not in data:
            return {'error': 'dept is required'}, 400
        dept = Department.query.filter(Department.name == data['dept']).one()
        res = Resource(
            title=data['title'],
            data=data['data'],
            description=data.get('description', 'Not detail'),
            department=dept,
            user=current_user
        )
        db.session.add(res)
        return res.to_dict()
    return jsonify([r.to_dict() for r in current_user.resources])
