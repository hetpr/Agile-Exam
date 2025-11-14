import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_status(client):
    res = client.get("/status")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}

def test_sum(client):
    res = client.get("/sum?a=1&b=2")
    assert res.status_code == 200
    assert res.get_json()["result"] == 3