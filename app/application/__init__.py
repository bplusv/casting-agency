import os

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from application import api
from application.models import db

migrate = Migrate()
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        cors.init_app(app)
        app.register_blueprint(api.bp)
    return app
