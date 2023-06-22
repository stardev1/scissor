def test_signup(client):
    response = client.post('/api/signup', json={'first_name': 'Test', 'last_name': 'User', 'email': 'testuser@example.com', 'password': 'testpassword'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['message'] == 'user created successfully'


def test_login(client):

    response = client.post('/api/signup', json={'first_name': 'Test', 'last_name': 'User', 'email': 'testuser@example.com', 'password': 'testpassword'})
    assert response.status_code == 201

    response = client.post('/api/login', json={'email': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 401

    response = client.post('/api/login', json={'notemail': 'testuser@example.com', 'password': 'testpassword'})
    assert response.status_code == 422

    response = client.post('/api/login', json={'email': 'testuser@example.com', 'password': 'testpassword'})
    assert response.status_code == 201

    data = response.get_json()
    assert 'token' in data
  