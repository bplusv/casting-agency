import os
from datetime import date

from jose import jwt
import pytest

from src.main import create_app
from src.models import db, Actor, Gender, Movie
from src.auth import Auth, UserRole


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
    class AuthFixture:
        @staticmethod
        def bearer_token(role):
            permissions = []
            if role == UserRole.CASTING_ASSISTANT:
                permissions = ['get:actor', 'get:actors', 'get:movie',
                               'get:movies']
            elif role == UserRole.CASTING_DIRECTOR:
                permissions = ['get:actor', 'get:actors', 'get:movie',
                               'get:movies', 'delete:actor', 'post:actor',
                               'patch:actor', 'patch:movie']
            elif role == UserRole.EXECUTIVE_PRODUCER:
                permissions = ['get:actor', 'get:actors', 'get:movie',
                               'get:movies', 'delete:actor', 'post:actor',
                               'patch:actor', 'patch:movie', 'delete:movie',
                               'post:movie']
            return f"Bearer {jwt.encode({'permissions': permissions}, 'key')}"

    monkeypatch.setattr(Auth, 'verify_decode_jwt',
                        lambda token: jwt.get_unverified_claims(token))
    return AuthFixture
