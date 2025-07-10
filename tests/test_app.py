import pytest
from my_flask import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data or b'game' in response.data.lower()

def test_username_page_get(client):
    """Тест страницы ввода имени (GET запрос)"""
    response = client.get('/username')
    assert response.status_code == 200
    assert 'Введите ваше имя' in response.data.decode('utf-8')

def test_username_page_post_empty(client):
    """Тест отправки пустого имени"""
    response = client.post('/username', data={'username': ''})
    assert response.status_code == 200
    assert b'empty' in response.data.lower() or b'cannot' in response.data.lower()

def test_username_page_post_valid(client):
    """Тест отправки валидного имени"""
    response = client.post('/username', data={'username': 'TestUser'}, follow_redirects=True)
    assert response.status_code == 200

def test_game_page_without_session(client):
    """Тест страницы игры без сессии"""
    response = client.get('/game')
    assert response.status_code == 302  # Редирект на /username

def test_game_page_with_session(client):
    """Тест страницы игры с сессией"""
    with client.session_transaction() as sess:
        sess['username'] = 'TestUser'
    
    response = client.get('/game')
    assert response.status_code == 200
    assert 'Угадай число' in response.data.decode('utf-8') or b'game' in response.data.lower()

def test_game_post_invalid_guess(client):
    """Тест отправки невалидного числа"""
    with client.session_transaction() as sess:
        sess['username'] = 'TestUser'
        sess['secret_number'] = 500
        sess['attempts'] = 0
    
    response = client.post('/game', data={'guess': 'invalid'})
    assert response.status_code == 200
    assert b'value' in response.data.lower() or b'correct' in response.data.lower()

def test_game_post_out_of_range(client):
    """Тест отправки числа вне диапазона"""
    with client.session_transaction() as sess:
        sess['username'] = 'TestUser'
        sess['secret_number'] = 500
        sess['attempts'] = 0
    
    response = client.post('/game', data={'guess': '1500'})
    assert response.status_code == 200
    assert 'от 1 до 1000' in response.data.decode('utf-8') 