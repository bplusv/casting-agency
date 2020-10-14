from flask_sqlalchemy import SQLAlchemy

from src.models import Movie
from src.auth import UserRole


db = SQLAlchemy()


def test_get_movie(client, auth):
    movie_id = 1
    res = client.get(f'/api/movies/{movie_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)})
    data = res.get_json()
    assert res.status_code == 200
    assert 'id' in data
    assert 'title' in data
    assert 'release_date' in data
    assert 'actors' in data


def test_get_movie_not_found(client, auth):
    movie_id = 99
    res = client.get(f'/api/movies/{movie_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)})
    data = res.get_json()
    assert res.status_code == 404
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_get_movies(client, auth):
    res = client.get('/api/movies', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, list)
    for movie in data:
        assert 'id' in movie
        assert 'title' in movie
        assert 'release_date' in movie
        assert 'actors' in movie


def test_get_movies_not_found(client, auth):
    Movie.query.delete()
    db.session.commit()
    res = client.get('/api/movies', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)})
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_delete_movie(client, auth):
    movie_id = 1
    res = client.delete(f'/api/movies/{movie_id}', headers={
        'Authorization': auth.bearer_token(UserRole.EXECUTIVE_PRODUCER)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert Movie.query.get(movie_id) is None


def test_delete_movie_not_found(client, auth):
    movie_id = 99
    res = client.delete(f'/api/movies/{movie_id}', headers={
        'Authorization': auth.bearer_token(UserRole.EXECUTIVE_PRODUCER)})
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_post_movie_without_actors(client, auth):
    post_data = {
        'title': 'blue ocean',
        'release_date': '1998-05-21'
    }
    res = client.post('/api/movies', json=post_data, headers={
        'Authorization': auth.bearer_token(UserRole.EXECUTIVE_PRODUCER)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert 'movie_id' in data
    movie = Movie.query.get(data['movie_id'])
    assert movie is not None
    assert movie.title == post_data['title']
    assert movie.release_date.date().isoformat() == post_data['release_date']


def test_post_movie_with_actors(client, auth):
    post_data = {
        'title': 'blue ocean',
        'release_date': '1998-05-21',
        'actors': [2, 1]
    }
    res = client.post('/api/movies', json=post_data, headers={
        'Authorization': auth.bearer_token(UserRole.EXECUTIVE_PRODUCER)})
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert 'movie_id' in data
    movie = Movie.query.get(data['movie_id'])
    assert movie is not None
    assert movie.title == post_data['title']
    assert movie.release_date.date().isoformat() == post_data['release_date']
    assert set(actor.id for actor in movie.actors) == set(post_data['actors'])


def test_post_movie_unprocessable(client, auth):
    post_data = {
        'title': 'another world 2',
        'release_date': None
    }
    res = client.post('/api/movies', json=post_data, headers={
        'Authorization': auth.bearer_token(UserRole.EXECUTIVE_PRODUCER)})
    data = res.get_json()
    assert res.status_code == 422
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 422
    assert data['message'] == 'Unprocessable entity'


def test_patch_movie_with_release_date(client, auth):
    movie_id = 1
    patch_data = {
        'release_date': '2022-12-01'
    }
    res = client.patch(f'/api/movies/{movie_id}', json=patch_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    movie = Movie.query.get(movie_id)
    assert movie.release_date.date().isoformat() == patch_data['release_date']


def test_patch_movie_with_title_actors(client, auth):
    movie_id = 1
    patch_data = {
        'title': 'Back to the future: part IV',
        'actors': [2, 1]
    }
    res = client.patch(f'/api/movies/{movie_id}', json=patch_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    movie = Movie.query.get(movie_id)
    assert movie.title == patch_data['title']
    assert set(actor.id for actor in movie.actors) == set(patch_data['actors'])


def test_patch_movie_not_found(client, auth):
    movie_id = 99
    patch_data = {
        'title': 'unkown future'
    }
    res = client.patch(f'/api/movies/{movie_id}', json=patch_data, headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)})
    data = res.get_json()
    assert res.status_code == 404
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'
