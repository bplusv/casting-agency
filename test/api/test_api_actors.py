from flask_sqlalchemy import SQLAlchemy

from src.models import Actor
from src.auth import UserRole


db = SQLAlchemy()


def test_get_actor(client, auth):
    actor_id = 1
    res = client.get(f'/api/actors/{actor_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)})
    data = res.get_json()
    assert res.status_code == 200
    assert 'name' in data
    assert 'age' in data
    assert 'gender' in data
    assert 'movies' in data


def test_get_actor_not_found(client, auth):
    actor_id = 99
    res = client.get(f'api/actors/{actor_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)})
    data = res.get_json()
    assert res.status_code == 404
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_get_actors(client, auth):
    res = client.get('/api/actors', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, list)
    for actor in data:
        assert 'name' in actor
        assert 'age' in actor
        assert 'gender' in actor
        assert 'movies' in actor


def test_get_actors_not_found(client, auth):
    Actor.query.delete()
    db.session.commit()
    res = client.get('/api/actors', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)})
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_delete_actor(client, auth):
    actor_id = 1
    res = client.delete(f'/api/actors/{actor_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert Actor.query.get(actor_id) is None


def test_delete_actor_not_found(client, auth):
    actor_id = 99
    res = client.delete(f'/api/actors/{actor_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_post_actor_without_movies(client, auth):
    post_data = {
        'name': 'Lisa Mcdowell',
        'age': 70,
        'gender': 'female'
    }
    res = client.post('/api/actors', json=post_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert 'actor_id' in data
    actor = Actor.query.get(data['actor_id'])
    assert actor is not None
    assert actor.name == post_data['name']
    assert actor.age == post_data['age']
    assert actor.gender.name.lower() == post_data['gender']


def test_post_actor_with_movies(client, auth):
    post_data = {
        'name': 'Lisa Mcdowell',
        'age': 70,
        'gender': 'female',
        'movies': [2, 1]
    }
    res = client.post('/api/actors', json=post_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert 'actor_id' in data
    actor = Actor.query.get(data['actor_id'])
    assert actor is not None
    assert actor.name == post_data['name']
    assert actor.age == post_data['age']
    assert actor.gender.name.lower() == post_data['gender']
    assert set(movie.id for movie in actor.movies) == set(post_data['movies'])


def test_post_actor_unprocessable(client, auth):
    post_data = {
        'name': 'Angela Rubius',
        'age': None,
        'gender': None
    }
    res = client.post('/api/actors', json=post_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 422
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 422
    assert data['message'] == 'Unprocessable entity'


def test_patch_actor_without_movies(client, auth):
    actor_id = 2
    patch_data = {
        'name': 'Jane Gainwell',
        'age': 21,
        'gender': 'female'
    }
    res = client.patch(f'/api/actors/{actor_id}', json=patch_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    actor = Actor.query.get(actor_id)
    assert actor.name == patch_data['name']
    assert actor.age == patch_data['age']
    assert actor.gender.name.lower() == patch_data['gender']


def test_patch_actor_with_movies(client, auth):
    actor_id = 2
    patch_data = {
        'name': 'Jane Gainwell',
        'age': 21,
        'gender': 'female',
        'movies': [2, 1]
    }
    res = client.patch(f'/api/actors/{actor_id}', json=patch_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    actor = Actor.query.get(actor_id)
    assert actor.name == patch_data['name']
    assert actor.age == patch_data['age']
    assert actor.gender.name.lower() == patch_data['gender']
    assert set(movie.id for movie in actor.movies) == set(patch_data['movies'])


def test_patch_actor_not_found(client, auth):
    actor_id = 99
    patch_data = {
        'age': 10
    }
    res = client.patch(f'/api/actors/{actor_id}', json=patch_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'
