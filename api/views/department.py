from flask import Blueprint, jsonify, request
from app import db

from models import Department


bp = Blueprint("department", __name__, url_prefix='/departments')


@bp.route("/")
def get_departments():
    all_departments = Department.query.all()
    return jsonify([i.to_dict() for i in all_departments])


@bp.route("/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_department(id):
    department = Department.query.filter(Department.id == id).first_or_404()
    if request.method == 'PUT':
        args = request.get_json()
        department.update(**args)
        db.session.commit()
    elif request.method == 'DELETE':
        db.session.delete(department)
        db.session.commit()
    return department.to_dict()
