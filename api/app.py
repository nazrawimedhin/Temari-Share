from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from os import getenv

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """configure app"""
    app = Flask(__name__)
    USER = getenv('DB_USER') or 'temari'
    PWD = getenv('DB_PWD') or 'temari_pwd'
    DB = getenv('DB_NAME') or 'temari_db'
    url = f'mysql://{USER}:{PWD}@localhost/{DB}'
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/status')
    def status():
        return {'status': 'OK'}

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not found(404)'}, 404

    @app.errorhandler(500)
    def server_err(e):
        return {'error': 'Internal Server Error(500)'}, 500

    from views import resources, users, department
    app.register_blueprint(resources.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(department.bp)

    return app
