import os
import enum

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    Migrate(app, db)


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2


movie_actors_table = db.Table(
    'movie_actors',
    db.Column('movie_id', db.Integer,
              db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer,
              db.ForeignKey('actors.id'), primary_key=True),
)


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    movies = db.relationship('Movie', secondary=movie_actors_table, lazy=True)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime(timezone=True), nullable=False)
    actors = db.relationship('Actor', secondary=movie_actors_table, lazy=True)
