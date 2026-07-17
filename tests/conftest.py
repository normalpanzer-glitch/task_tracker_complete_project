import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture(autouse=True)
def reset_storage() -> None:
    storage._reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def created_task(client: TestClient) -> dict:
    response = client.post("/tasks", json={"title": "Course task"})
    assert response.status_code == 201
    return response.json()
