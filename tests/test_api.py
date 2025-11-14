import threading
import time
import requests
import pytest
from app import app

BASE = "http://127.0.0.1:5000"

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

def test_status():
    r = requests.get(f"{BASE}/status")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_sum():
    r = requests.get(f"{BASE}/sum?a=2&b=3")
    assert r.status_code == 200
    assert r.json()["result"] == 5