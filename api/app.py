from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from os import getenv

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    USER = getenv('DB_USER') or 'temari'
    PWD = getenv('DB_PWD') or 'temari_pwd'
    DB = getenv('DB_NAME') or 'temari_db'
    url = f'mysql://{USER}:{PWD}@localhost/{DB}'
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    Migrate(app, db)

    @app.route('/status')
    def status():
        return {'status': 'OK'}

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'not found(404)'}, 404

    from views import resources
    app.register_blueprint(resources.bp)

    return app
