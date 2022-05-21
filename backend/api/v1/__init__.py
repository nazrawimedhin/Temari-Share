from flask import Blueprint
from .views import resources, users, department


bp = Blueprint("api", __name__, url_prefix='/api')
bp.register_blueprint(resources.bp)
bp.register_blueprint(users.bp)
bp.register_blueprint(department.bp)
