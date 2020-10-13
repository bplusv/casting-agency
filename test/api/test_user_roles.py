from src.auth import UserRole


def test_no_token_get_actors_forbidden(client):
    assert client.get('/api/actors').status_code == 401


def test_no_token_get_movies_forbidden(client):
    assert client.get('/api/movies').status_code == 401


def test_casting_assistant_get_movies_authorized(client, auth):
    assert client.get('/api/movies', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)
    }).status_code == 200


def test_casting_assistant_delete_actor_forbidden(client, auth):
    actor_id = 1
    assert client.delete(f'/api/actors/{actor_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_ASSISTANT)
    }).status_code == 403


def test_casting_director_delete_actor_permitted(client, auth):
    actor_id = 1
    assert client.delete(f'/api/actors/{actor_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)
    }).status_code == 200


def test_casting_director_delete_movie_forbidden(client, auth):
    movie_id = 1
    assert client.delete(f'/api/movies/{movie_id}', headers={
        'Authorization': auth.bearer_token(UserRole.CASTING_DIRECTOR)
    }).status_code == 403


def test_executive_producer_delete_movie_permitted(client, auth):
    movie_id = 1
    assert client.delete(f'/api/movies/{movie_id}', headers={
        'Authorization': auth.bearer_token(UserRole.EXECUTIVE_PRODUCER)
    }).status_code == 200


def test_executive_producer_post_movie_permitted(client, auth):
    post_data = {
        'title': 'Tokyo 2020',
        'release_date': '2021-04-01'
    }
    assert client.post('/api/movies', json=post_data, headers={
        'Authorization': auth.bearer_token(UserRole.EXECUTIVE_PRODUCER)
    }).status_code == 200
