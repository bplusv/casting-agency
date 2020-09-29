import os

import pytest

from application import create_app
from application.models import db, Actor, Gender


def seed_db():
    Actor('Joe Gainwell', 23, Gender.MALE).insert()
    Actor('Michelle Ortega', 19, Gender.FEMALE).insert()


@pytest.fixture
def client():
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        seed_db()
    return app.test_client()
