import threading, time, requests, pytest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture(scope="session", autouse=True)
def start_server():
    thread = threading.Thread(
        target=app.run,
        kwargs={"host": "127.0.0.1", "port": 5000, "use_reloader": False},
        daemon=True,
    )
    thread.start()
    time.sleep(1)
    yield

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