import pytest
from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}


def test_valid_message(client):
    response = client.post('/api/validate', json={'message': 'hello'})
    assert response.status_code == 200
    assert response.json == {'valid': True, 'length': 5}


@pytest.mark.parametrize('message', ['', ' ', 'a' * 201])
def test_reject_invalid_length(client, message):
    response = client.post('/api/validate', json={'message': message})
    assert response.status_code == 400


def test_reject_bad_type(client):
    assert client.post('/api/validate', json={'message': 12}).status_code == 400


def test_reject_wrong_content_type(client):
    assert client.post('/api/validate', data='hello', content_type='text/plain').status_code == 415


def test_security_headers(client):
    response = client.get('/health')
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert response.headers['X-Frame-Options'] == 'DENY'
    assert response.headers['Cache-Control'] == 'no-store'
