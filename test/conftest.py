import os
from datetime import date

from jose import jwt
import pytest

from src.main import create_app
from src.models import db, Actor, Gender, Movie
from src.auth import Auth


def seed_db():
    Actor('Joe Gainwell', 23, Gender.MALE).insert()
    Actor('Michelle Ortega', 19, Gender.FEMALE).insert()
    Movie('Back to the future 4', date.fromisoformat('2021-04-01')).insert()
    Movie('A new bright sunshine', date.fromisoformat('2022-09-01')).insert()


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


@pytest.fixture
def auth(monkeypatch):
    bearer_header = jwt.encode({'permissions': ['get:actors']}, 'secret')
    monkeypatch.setattr(Auth, 'get_token_auth_header',
                        lambda: bearer_header)
    monkeypatch.setattr(Auth, 'verify_decode_jwt',
                        lambda token: jwt.get_unverified_claims(token))
