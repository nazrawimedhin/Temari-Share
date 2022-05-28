from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from .auth import admin_only

from models import Department


bp = Blueprint("department", __name__, url_prefix='/departments')


@bp.route("/")
def get_departments():
    all_departments = Department.query.all()
    return jsonify([i.to_dict() for i in all_departments])


@bp.route("/<int:id>")
def get_department(id):
    department = Department.query.filter(Department.id == id).first_or_404()
    return department.to_dict()


@bp.route("/<int:id>", methods=['PUT', 'DELETE'])
@jwt_required
@admin_only
def mod_departement(id):
    department = Department.query.filter(Department.id == id).first_or_404()
    if request.method == 'PUT':
        args = request.get_json()
        department.update(**args)
    elif request.method == 'DELETE':
        db.session.delete(department)
