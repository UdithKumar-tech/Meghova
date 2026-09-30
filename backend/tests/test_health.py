from fastapi.testclient import TestClient
from app.main import app


def test_root_and_health():
    client = TestClient(app)
    root = client.get('/api')
    assert root.status_code == 200
    health = client.get('/api/health')
    assert health.status_code == 200
    data = health.json()
    assert 'model_ready' in data
