import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_generate_unauthorized():
    resp = client.post("/quiz/generate", json={"topic":"math","num_questions":2,"difficulty":"easy"})
    assert resp.status_code == 422  # missing header

def test_eval_dummy():
    quiz = [
        {"question":"2+2","options":["3","4"],"answer":"4"}
    ]
    responses = ["4"]
    resp = client.post("/quiz/evaluate", headers={"x-api-key":"change_me_long_random"}, json={"quiz":quiz,"responses":responses})
    assert resp.status_code == 200
    result = resp.json()
    assert result["score"] == 1
    assert result["total"] == 1
