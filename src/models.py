import enum

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender.name.lower(),
            'movies': [movie.id for movie in self.movies]
        }


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime(timezone=True), nullable=False)
    actors = db.relationship('Actor', secondary=movie_actors_table, lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.id for actor in self.actors]
        }
