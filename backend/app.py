from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, get_jwt, create_access_token,
    get_jwt_identity, set_access_cookies)
from datetime import datetime, timedelta, timezone
from os import getenv

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    """configure app"""
    app = Flask(__name__)
    USER = getenv('DB_USER') or 'temari'
    PWD = getenv('DB_PWD') or 'temari_pwd'
    DB = getenv('DB_NAME') or 'temari_db'
    url = f'mysql://{USER}:{PWD}@localhost/{DB}'
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = getenv('SECRET_KEY') or 'dev'
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]

    # change this to true on production
    app.config["JWT_COOKIE_SECURE"] = False
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route('/status')
    def status():
        return {'status': 'OK'}

    @app.teardown_appcontext
    def commit_db(e):
        """commits any modification"""
        db.session.commit()

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        from models import User
        return User.query.filter_by(username=identity).one_or_none()

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT
            return response

    from api import v1
    import auth
    import views
    app.register_blueprint(v1.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='index')

    return app
