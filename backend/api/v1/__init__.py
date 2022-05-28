from flask import Blueprint, jsonify
from .views import resources, users, department, auth


bp = Blueprint("api", __name__, url_prefix='/api')
bp.register_blueprint(resources.bp)
bp.register_blueprint(users.bp)
bp.register_blueprint(department.bp)
bp.register_blueprint(auth.bp)


@bp.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@bp.errorhandler(500)
def server_err(e):
    return jsonify(error=str(e)), 500
