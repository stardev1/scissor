


from flask import jsonify

from flask_jwt_extended import create_access_token

UUID = "31956c72-0df8-11ee-be56-0242ac120002"

def test_index(client, app):
    response = client.get('/api/')
    assert response.status_code == 401

    with app.app_context():
        access_token = create_access_token(identity=UUID)

    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/api/', headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data['status'] == 'ok'
    assert isinstance(data['total'], int)
    assert isinstance(data['page'], int)
    assert isinstance(data['per_page'], int)
    assert isinstance(data['data'], list)


def test_create(client, app):

    with app.app_context():
        access_token = create_access_token(identity=UUID)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/api/generate', json={'url': 'https://www.example.com'}, headers = headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'ok'
    assert isinstance(data['data'], dict)
    assert data['message'] == 'url created'
    assert isinstance(data['limit'], str)

def test_url(client, app):

    with app.app_context():
        access_token = create_access_token(identity=UUID)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/api/someurl', headers = headers)

    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['message'] == 'url not found'


def test_create_custom_url(client, app):

    with app.app_context():
        access_token = create_access_token(identity=UUID)

    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/api/generate', json={'url': 'https://www.example.com', 'custom_url': 'someurl'}, headers = headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'ok'
    assert isinstance(data['data'], dict)
    assert data['message'] == 'url created'
    assert isinstance(data['limit'], str)


def test_custom_url(client, app):

    with app.app_context():
        access_token = create_access_token(identity=UUID)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.post('/api/generate', json={'url': 'https://www.example.com', 'custom_url': 'someurl'}, headers = headers)
    assert response.status_code == 201

    response = client.get('/api/someurl', headers = headers)

    assert response.status_code == 200
    data = response.get_json()
   
    assert type(data) == dict


def test_visitors(client, app):

    with app.app_context():
        access_token = create_access_token(identity=UUID)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.post('/api/generate', json={'url': 'https://www.example.com', 'custom_url': 'someurl'}, headers = headers)
    assert response.status_code == 201

    response = client.get('api/someurl/visitors', headers = headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert isinstance(data['total'], int)
    assert isinstance(data['page'], int)
    assert isinstance(data['per_page'], int)
    assert isinstance(data['data'], list)


def test_edit(client, app):
    with app.app_context():
        access_token = create_access_token(identity=UUID)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.post('/api/generate', json={'url': 'https://www.example.com', 'custom_url': 'someurl'}, headers = headers)
    assert response.status_code == 201

    response = client.patch('/api/someurl/edit', json={'url': 'https://www.example.com', 'custom_url': 'testurl'}, headers = headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['message'] == 'URL updated successfully'

def test_delete_owner(client, app):

    with app.app_context():
        access_token = create_access_token(identity="random user")
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.post('/api/generate', json={'url': 'https://www.example.com', 'custom_url': 'someurl'}, headers = headers)
    assert response.status_code == 201

    with app.app_context():
        access_token = create_access_token(identity=UUID)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.delete('/api/someurl/delete', headers = headers)
    assert response.status_code == 403
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['message'] == 'you are not allowed to delete this url'

def test_delete(client, app):
    with app.app_context():
        access_token = create_access_token(identity=UUID)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.post('/api/generate', json={'url': 'https://www.example.com', 'custom_url': 'someurl'}, headers = headers)
    assert response.status_code == 201

    response = client.delete('/api/someurl/delete', headers = headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['message'] == 'URL deleted successfully'

