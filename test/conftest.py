import os
from datetime import date

import pytest

from src.main import create_app
from src.models import db, Actor, Gender, Movie


def seed_db():
    actor1 = Actor('Joe Gainwell', 23, Gender.MALE).insert()
    actor2 = Actor('Michelle Ortega', 19, Gender.FEMALE).insert()
    movie1 = Movie('Back to the future 4',
                   date.fromisoformat('2021-04-01')).insert()
    movie1.actors = [actor1, actor2]
    movie1.update()


@pytest.fixture
def client():
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            seed_db()
            yield client
