import pytest

from app.main import app, todos


@pytest.fixture
def client():
    todos.clear()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_is_empty_at_start(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_todo(client):
    response = client.post("/todos", json={"title": "Learn GitHub Actions"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Learn GitHub Actions"
    assert len(client.get("/todos").get_json()) == 1


def test_add_todo_without_title(client):
    response = client.post("/todos", json={})
    assert response.status_code == 400


def test_second_todo_gets_id_2(client):
    first = client.post("/todos", json={"title": "First todo"})
    assert first.status_code == 201
    assert first.get_json()["id"] == 1

    second = client.post("/todos", json={"title": "Second todo"})
    assert second.status_code == 201
    assert second.get_json()["id"] == 2

    todos_list = client.get("/todos").get_json()
    assert len(todos_list) == 2
    assert todos_list[0]["id"] == 1
    assert todos_list[1]["id"] == 2