import pytest
from fastapi.testclient import TestClient
from main import app
from schemas import AgentQuery
import json
from pydantic import ValidationError

client = TestClient(app)

def test_login():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_invalid_login():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401

def test_secure_data_with_token():
    login_response = client.post(
        "/token",
        data={"username": "admin", "password": "secret"},
    )
    token = login_response.json()["access_token"]
    
    response = client.get("/secure-data", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello admin, you are authenticated."}

def test_secure_data_without_token():
    response = client.get("/secure-data")
    assert response.status_code == 401

def test_pydantic_sanitization():
    query = AgentQuery(query="What are the incidents?")
    assert query.query == "What are the incidents?"
    
    with pytest.raises(ValidationError):
        AgentQuery(query="")
