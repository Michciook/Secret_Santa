import pytest
from website import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_secret_key"
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        if app.config['TESTING']:
            db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_register(client):
    response = client.post('/api/auth/register/', json={
        'username': 'test',
        'email': 'test@test.me',
        'password': 'Test123'
    })
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['message'] == 'User registered successfully!'


def test_register_same_email(client):
    client.post('/api/auth/register/', json={
        'username': 'test',
        'email': 'test@test.me',
        'password': 'Test123'
    })

    response = client.post('/api/auth/register/', json={
        'username': 'newtest',
        'email': 'test@test.me',
        'password': 'Test123'
    })

    json_data = response.get_json()
    assert response.status_code == 408
    assert json_data['error'] == 'User with this username or email already exists!'


def test_register_same_username(client):
    client.post('/api/auth/register/', json={
        'username': 'test',
        'email': 'test@test.me',
        'password': 'Test123'
    })

    response = client.post('/api/auth/register/', json={
        'username': 'test',
        'email': 'newtest@test.me',
        'password': 'Test123'
    })

    json_data = response.get_json()
    assert response.status_code == 408
    assert json_data['error'] == 'User with this username or email already exists!'


def test_register_no_data(client):
    response = client.post('/api/auth/register/', json={})
     
    json_data = response.get_json()
    assert response.status_code == 401
    assert json_data['error'] == 'Username and password is required!'


def test_login(client):
    client.post('/api/auth/register/', json={
        'username': 'test',
        'email': 'test@test.me',
        'password': 'Test123'
    })

    response = client.post('/api/auth/login/', json={
        'username': 'test',
        'password': 'Test123'
    })

    json_data = response.get_json()
    assert response.status_code == 200
    assert 'id' in json_data
    assert json_data['name'] == 'test'


def test_login_wrong_password(client):
    client.post('/api/auth/register/', json={
        'username': 'test',
        'email': 'test@test.me',
        'password': 'Test123'
    })

    response = client.post('/api/auth/login/', json={
        'username': 'test',
        'password': 'wrong'
    })

    json_data = response.get_json()
    assert response.status_code == 401
    assert json_data['error'] == 'Wrong password'


def test_login_no_user(client):
    response = client.post('/api/auth/login/', json={
        'username': 'test',
        'password': 'wrong'
    })
     
    json_data = response.get_json()
    assert response.status_code == 401
    assert json_data['error'] == 'No user found'


def test_login_no_data(client):
    response = client.post('/api/auth/login/', json={})
     
    json_data = response.get_json()
    assert response.status_code == 401
    assert json_data['error'] == 'Username and password is required!'


def test_logout(client):
    client.post('/api/auth/register/', json={
        'username': 'test',
        'email': 'test@test.me',
        'password': 'Test123'
    })

    client.post('/api/auth/login/', json={
        'username': 'test',
        'password': 'Test123'
    })

    response = client.post('/api/auth/logout/')
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['message'] == 'Logged out'


def test_logout_without_login(client):
    response = client.post('/api/auth/logout/')
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['message'] == 'Login first!'


def test_get_rooms_without_login(client):
    response = client.get('/api/get_rooms/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data == {'message': 'Login first!'}