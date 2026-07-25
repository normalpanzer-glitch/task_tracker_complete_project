from fastapi.testclient import TestClient
from datetime import date, timedelta


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_returns_201_and_defaults(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "  First task  "})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "First task"
    assert body["description"] == ""
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["id"]
    assert body["created_at"] == body["updated_at"]


def test_create_rejects_missing_title(client: TestClient) -> None:
    assert client.post("/tasks", json={}).status_code == 422


def test_create_rejects_blank_title(client: TestClient) -> None:
    assert client.post("/tasks", json={"title": "   "}).status_code == 422


def test_create_rejects_overlong_title(client: TestClient) -> None:
    assert client.post("/tasks", json={"title": "x" * 201}).status_code == 422


def test_create_rejects_extra_and_server_fields(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Task", "id": "client-id"})
    assert response.status_code == 422


def test_create_rejects_invalid_enums(client: TestClient) -> None:
    assert client.post("/tasks", json={"title": "Task", "status": "Started"}).status_code == 422
    assert client.post("/tasks", json={"title": "Task", "priority": "Urgent"}).status_code == 422


def test_list_empty_returns_200(client: TestClient) -> None:
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_returns_created_tasks(client: TestClient, created_task: dict) -> None:
    response = client.get("/tasks")
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [created_task["id"]]


def test_list_filters_by_status_and_priority(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Low", "priority": "Low"})
    client.post("/tasks", json={"title": "High", "priority": "High"})
    assert [t["title"] for t in client.get("/tasks", params={"priority": "High"}).json()] == ["High"]
    assert len(client.get("/tasks", params={"status": "ToDo"}).json()) == 2


def test_get_existing_task(client: TestClient, created_task: dict) -> None:
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json() == created_task


def test_get_missing_task_returns_404(client: TestClient) -> None:
    response = client.get("/tasks/missing")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing not found"


def test_patch_title_updates_task(client: TestClient, created_task: dict) -> None:
    response = client.patch(f"/tasks/{created_task['id']}", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_patch_rejects_blank_title(client: TestClient, created_task: dict) -> None:
    response = client.patch(f"/tasks/{created_task['id']}", json={"title": " "})
    assert response.status_code == 422


def test_patch_rejects_null_title_without_changing_task(client: TestClient, created_task: dict) -> None:
    response = client.patch(f"/tasks/{created_task['id']}", json={"title": None})
    assert response.status_code == 422
    assert "Title cannot be null" in response.json()["detail"][0]["msg"]
    assert client.get(f"/tasks/{created_task['id']}").json()["title"] == created_task["title"]


def test_patch_rejects_null_status_without_changing_task(client: TestClient, created_task: dict) -> None:
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": None})
    assert response.status_code == 422
    assert "Status cannot be null" in response.json()["detail"][0]["msg"]
    assert client.get(f"/tasks/{created_task['id']}").json()["status"] == created_task["status"]


def test_patch_missing_task_returns_404(client: TestClient) -> None:
    assert client.patch("/tasks/missing", json={"title": "Updated"}).status_code == 404


def test_valid_todo_to_in_progress(client: TestClient, created_task: dict) -> None:
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_valid_in_progress_to_done(client: TestClient, created_task: dict) -> None:
    task_id = created_task["id"]
    assert client.patch(f"/tasks/{task_id}", json={"status": "InProgress"}).status_code == 200
    response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert response.status_code == 200


def test_valid_done_to_in_progress(client: TestClient, created_task: dict) -> None:
    task_id = created_task["id"]
    client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert client.patch(f"/tasks/{task_id}", json={"status": "InProgress"}).status_code == 200


def test_invalid_todo_to_done_returns_422(client: TestClient, created_task: dict) -> None:
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": "Done"})
    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_same_status_transition_returns_422(client: TestClient, created_task: dict) -> None:
    assert client.patch(f"/tasks/{created_task['id']}", json={"status": "ToDo"}).status_code == 422


def test_delete_existing_returns_empty_204(client: TestClient, created_task: dict) -> None:
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{created_task['id']}").status_code == 404


def test_delete_missing_returns_404(client: TestClient) -> None:
    assert client.delete("/tasks/missing").status_code == 404


def test_cors_allows_local_frontend(client: TestClient) -> None:
    response = client.options(
        "/tasks",
        headers={
            "Origin": "http://localhost:5500",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5500"


def test_create_task_with_due_date(client: TestClient) -> None:
    due_date = (date.today() + timedelta(days=3)).isoformat()
    response = client.post("/tasks", json={"title": "Dated task", "due_date": due_date})
    assert response.status_code == 201
    assert response.json()["due_date"] == due_date


def test_invalid_due_date_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Bad date", "due_date": "tomorrow"})
    assert response.status_code == 422


def test_update_due_date_preserves_other_fields(client: TestClient, created_task: dict) -> None:
    due_date = (date.today() + timedelta(days=5)).isoformat()
    response = client.patch(f"/tasks/{created_task['id']}", json={"due_date": due_date})
    assert response.status_code == 200
    assert response.json()["title"] == created_task["title"]
    assert response.json()["due_date"] == due_date


def test_overdue_filter_excludes_done_tasks(client: TestClient) -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    overdue = client.post("/tasks", json={"title": "Overdue", "due_date": yesterday}).json()
    done = client.post("/tasks", json={"title": "Completed", "due_date": yesterday}).json()
    client.patch(f"/tasks/{done['id']}", json={"status": "InProgress"})
    client.patch(f"/tasks/{done['id']}", json={"status": "Done"})
    response = client.get("/tasks", params={"overdue": "true"})
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [overdue["id"]]


def test_search_matches_title_and_description(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Prepare report", "description": "Finance review"})
    client.post("/tasks", json={"title": "Call client", "description": "Discuss launch"})
    assert [task["title"] for task in client.get("/tasks", params={"search": "REPORT"}).json()] == ["Prepare report"]
    assert [task["title"] for task in client.get("/tasks", params={"search": "launch"}).json()] == ["Call client"]


def test_combined_search_priority_and_assignee_filters(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Release docs", "priority": "High", "assignee": "Maya"})
    client.post("/tasks", json={"title": "Release notes", "priority": "Low", "assignee": "Maya"})
    client.post("/tasks", json={"title": "Release build", "priority": "High", "assignee": "Omar"})
    response = client.get("/tasks", params={"search": "release", "priority": "High", "assignee": "maya"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Release docs"]


def test_search_no_matches_returns_empty_list(client: TestClient, created_task: dict) -> None:
    response = client.get("/tasks", params={"search": "not-present"})
    assert response.status_code == 200
    assert response.json() == []
