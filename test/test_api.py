from flask_sqlalchemy import SQLAlchemy

from src.models import Actor, Movie


db = SQLAlchemy()


def test_get_actor(client):
    actor_id = 1
    res = client.get(f'/api/actors/{actor_id}')
    data = res.get_json()
    assert res.status_code == 200
    assert 'name' in data
    assert 'age' in data
    assert 'gender' in data
    assert 'movies' in data


def test_get_actor_not_found(client):
    actor_id = 99
    res = client.get(f'api/actors/{actor_id}')
    data = res.get_json()
    assert res.status_code == 404
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_get_actors(client, auth):
    res = client.get('/api/actors')
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


def test_post_actor_without_movies(client):
    post_data = {
        'name': 'Lisa Mcdowell',
        'age': 70,
        'gender': 'female'
    }
    res = client.post('/api/actors', json=post_data)
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


def test_post_actor_with_movies(client):
    post_data = {
        'name': 'Lisa Mcdowell',
        'age': 70,
        'gender': 'female',
        'movies': [2, 1]
    }
    res = client.post('/api/actors', json=post_data)
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


def test_post_actor_unprocessable(client):
    post_data = {
        'name': 'Angela Rubius',
        'age': None,
        'gender': None
    }
    res = client.post('/api/actors', json=post_data)
    data = res.get_json()
    assert res.status_code == 422
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 422
    assert data['message'] == 'Unprocessable entity'


def test_patch_actor_without_movies(client):
    actor_id = 2
    patch_data = {
        'name': 'Jane Gainwell',
        'age': 21,
        'gender': 'female'
    }
    res = client.patch(f'/api/actors/{actor_id}', json=patch_data)
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    actor = Actor.query.get(actor_id)
    assert actor.name == patch_data['name']
    assert actor.age == patch_data['age']
    assert actor.gender.name.lower() == patch_data['gender']


def test_patch_actor_with_movies(client):
    actor_id = 2
    patch_data = {
        'name': 'Jane Gainwell',
        'age': 21,
        'gender': 'female',
        'movies': [2, 1]
    }
    res = client.patch(f'/api/actors/{actor_id}', json=patch_data)
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    actor = Actor.query.get(actor_id)
    assert actor.name == patch_data['name']
    assert actor.age == patch_data['age']
    assert actor.gender.name.lower() == patch_data['gender']
    assert set(movie.id for movie in actor.movies) == set(patch_data['movies'])


def test_patch_actor_not_found(client):
    actor_id = 99
    patch_data = {
        'age': 10
    }
    res = client.patch(f'/api/actors/{actor_id}', json=patch_data)
    data = res.get_json()
    assert res.status_code == 404
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'


def test_get_movie(client):
    movie_id = 1
    res = client.get(f'/api/movies/{movie_id}')
    data = res.get_json()
    assert res.status_code == 200
    assert 'title' in data
    assert 'release_date' in data
    assert 'actors' in data


def test_get_movie_not_found(client):
    movie_id = 99
    res = client.get(f'/api/movies/{movie_id}')
    data = res.get_json()
    assert res.status_code == 404
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
        assert 'actors' in movie


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


def test_post_movie_without_actors(client):
    post_data = {
        'title': 'blue ocean',
        'release_date': '1998-05-21'
    }
    res = client.post('/api/movies', json=post_data)
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, dict)
    assert data['success'] is True
    assert 'movie_id' in data
    movie = Movie.query.get(data['movie_id'])
    assert movie is not None
    assert movie.title == post_data['title']
    assert movie.release_date.date().isoformat() == post_data['release_date']


def test_post_movie_with_actors(client):
    post_data = {
        'title': 'blue ocean',
        'release_date': '1998-05-21',
        'actors': [2, 1]
    }
    res = client.post('/api/movies', json=post_data)
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


def test_post_movie_unprocessable(client):
    post_data = {
        'title': 'another world 2',
        'release_date': None
    }
    res = client.post('/api/movies', json=post_data)
    data = res.get_json()
    assert res.status_code == 422
    assert isinstance(data, dict)
    assert data['success'] is False
    assert data['error'] == 422
    assert data['message'] == 'Unprocessable entity'


def test_patch_movie_without_actors(client):
    movie_id = 1
    patch_data = {
        'title': 'Back to the future: part IV',
        'release_date': '2022-12-01'
    }
    res = client.patch(f'/api/movies/{movie_id}', json=patch_data)
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    movie = Movie.query.get(movie_id)
    assert movie.title == patch_data['title']
    assert movie.release_date.date().isoformat() == patch_data['release_date']


def test_patch_movie_with_actors(client):
    movie_id = 1
    patch_data = {
        'title': 'Back to the future: part IV',
        'release_date': '2022-12-01',
        'actors': [2, 1]
    }
    res = client.patch(f'/api/movies/{movie_id}', json=patch_data)
    data = res.get_json()
    assert res.status_code == 200
    assert data['success'] is True
    movie = Movie.query.get(movie_id)
    assert movie.title == patch_data['title']
    assert movie.release_date.date().isoformat() == patch_data['release_date']
    assert set(actor.id for actor in movie.actors) == set(patch_data['actors'])


def test_patch_movie_not_found(client):
    movie_id = 99
    patch_data = {
        'title': 'unkown future'
    }
    res = client.patch(f'/api/movies/{movie_id}', json=patch_data)
    data = res.get_json()
    assert res.status_code == 404
    assert data['success'] is False
    assert data['error'] == 404
    assert data['message'] == 'Entity not found'
