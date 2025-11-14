import threading
import time
import requests
import pytest
from app import app

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
BASE_URL = f'http://{SERVER_HOST}:{SERVER_PORT}'

@pytest.fixture(scope='session', autouse=True)
def start_server():
    server = threading.Thread(target=app.run, kwargs={
        'host': SERVER_HOST, 'port': SERVER_PORT, 'debug': False, 'use_reloader': False
    })
    server.daemon = True
    server.start()

    for _ in range(20):
        try:
            requests.get(f'{BASE_URL}/status', timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    else:
        pytest.exit('Could not start Flask server for tests')
    yield

def test_status_endpoint():
    r = requests.get(f'{BASE_URL}/status', timeout=2)
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

@pytest.mark.parametrize('a,b,expected', [
    ('1', '2', 3.0),
    ('2.5', '0.5', 3.0),
    ('-1', '1', 0.0),
])
def test_sum_valid(a, b, expected):
    r = requests.get(f'{BASE_URL}/sum', params={'a': a, 'b': b}, timeout=2)
    assert r.status_code == 200
    assert abs(r.json().get('result') - expected) < 1e-9

def test_sum_invalid():
    r = requests.get(f'{BASE_URL}/sum', params={'a': 'x', 'b': 'y'}, timeout=2)
    assert r.status_code == 400
    assert 'error' in r.json()