from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, current_user
from app import db

from models import Resource, Role, User


bp = Blueprint("resources", __name__, url_prefix='/resource')


@bp.route("/")
def get_resources():
    all_resources = Resource.query.all()
    return jsonify([i.to_dict() for i in all_resources])


@bp.route("/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_resource(id):
    resource = Resource.query.filter(Resource.id == id).first_or_404()
    return resource.to_dict()


@bp.route("/<int:id>", methods=['PUT', 'DELETE'])
@jwt_required
def update_delete_resource(id):
    resource = Resource.query.filter(Resource.id == id).first_or_404()
    if current_user.id != resource.user_id or is_admin(current_user.id):
        abort(400)
    if request.method == 'PUT':
        args = request.get_json()
        resource.update(**args)
    elif request.method == 'DELETE':
        db.session.delete(resource)


def is_admin(id):
    admin = Role.query.filter(Role.name == 'admin')
    user = User.query.filter(User.id == id)
    return user.role == admin
