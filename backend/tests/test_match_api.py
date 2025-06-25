import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_match_query():
    res = client.post("/api/match", json={"query": "python developer"})
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for item in data:
        assert "title" in item and "score" in item