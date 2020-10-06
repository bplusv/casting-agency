from flask_sqlalchemy import SQLAlchemy

from src.models import Actor, Movie


db = SQLAlchemy()


def test_get_actors(client):
    res = client.get('/api/actors')
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, list)
    for actor in data:
        assert 'name' in actor
        assert 'age' in actor
        assert 'gender' in actor


def test_get_actors_not_found(client):
    Actor.query.delete()
    db.session.commit()
    res = client.get('/api/actors')
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_delete_actor(client):
    actor_id = 1
    res = client.delete(f'/api/actors/{actor_id}')
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert Actor.query.get(actor_id) is None


def test_delete_actor_not_found(client):
    actor_id = 99
    res = client.delete(f'/api/actors/{actor_id}')
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_get_movies(client):
    res = client.get('/api/movies')
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, list)
    for movie in data:
        assert 'title' in movie
        assert 'release_date' in movie


def test_get_movies_not_found(client):
    Movie.query.delete()
    db.session.commit()
    res = client.get('/api/movies')
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_delete_movie(client):
    movie_id = 1
    res = client.delete(f'/api/movies/{movie_id}')
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert Movie.query.get(movie_id) is None


def test_delete_movie_not_found(client):
    movie_id = 99
    res = client.delete(f'/api/movies/{movie_id}')
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'
