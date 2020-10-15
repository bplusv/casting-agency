from jose import jwt


def test_no_auth_header(client):
    res = client.get('/api/actors')
    data = res.get_json()
    assert res.status_code == 401
    assert data['message'] == 'Unauthorized: Authorization header is expected'


def test_no_bearer_in_auth_header(client):
    res = client.get('/api/actors', headers={
        'Authorization': "token"
    })
    data = res.get_json()
    assert res.status_code == 401
    assert data['message'] == ('Unauthorized: Authorization header '
                               'must start with bearer')


def test_no_token_in_auth_header(client):
    res = client.get('/api/actors', headers={
        'Authorization': "Bearer"
    })
    data = res.get_json()
    assert res.status_code == 401
    assert data['message'] == 'Unauthorized: Token not found'


def test_invalid_bearer_token_in_auth_header(client):
    res = client.get('/api/actors', headers={
        'Authorization': "Bearer token other"
    })
    data = res.get_json()
    assert res.status_code == 401
    assert data['message'] == ('Unauthorized: Authorization header '
                               'must be bearer token')


def test_no_permissions_payload_in_token(client, auth):
    token = jwt.encode({}, 'key')
    res = client.get('/api/actors', headers={
        'Authorization': f"Bearer {token}"
    })
    data = res.get_json()
    assert res.status_code == 403
    assert data['message'] == 'Forbidden: Permissions payload missing'


def test_unable_to_find_key_auth0_validation(client):
    token = jwt.encode({}, 'key', headers={'kid': 'secretkey'})
    res = client.get('/api/actors', headers={
        'Authorization': f"Bearer {token}"
    })
    data = res.get_json()
    assert res.status_code == 401
    assert data['message'] == ('Unauthorized: JWT unable to '
                               'find appropriate key')


def test_unable_to_parse_token_auth0_validation(client):
    token = jwt.encode({}, 'key', headers={
        'kid': '82iulBJoaXnwGRRJxUbRX'})
    res = client.get('/api/actors', headers={
        'Authorization': f"Bearer {token}"
    })
    data = res.get_json()
    assert res.status_code == 401
    assert data['message'] == 'Unauthorized: JWT Unable to parse token'
