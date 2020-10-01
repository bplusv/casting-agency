from os import getenv

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS


from src.models import db
from src.api import bp as api_bp


migrate = Migrate()
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        cors.init_app(app)
        app.register_blueprint(api_bp)
    return app
