from application.models import Actor, Gender


def test_get_actors(client):
    res = client.get('/api/actors')
    data = res.get_json()
    assert res.status_code == 200
    assert isinstance(data, list)
    for actor in data:
        assert 'name' in actor
        assert 'age' in actor
        assert 'gender' in actor
