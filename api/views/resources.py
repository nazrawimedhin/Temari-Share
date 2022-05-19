from flask import Blueprint, jsonify, request
from app import db

from models.Resource import Resource


bp = Blueprint("resource", __name__, url_prefix='/resource')


@bp.route("/", methods=['GET'])
def get_resources():
    all_resources = Resource.query.all()
    return jsonify([i.to_dict() for i in all_resources])


@bp.route("/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_resource(id):
    resource = Resource.query.filter(Resource.id == id).first_or_404()
    if request.method == 'PUT':
        resource.update()
    elif request.method == 'DELETE':
        db.session.delete(resource)
        db.session.commit()
    return resource.to_dict()
