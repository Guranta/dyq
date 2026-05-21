from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_providers_contains_mock() -> None:
    response = client.get("/api/v1/providers")
    assert response.status_code == 200
    items = response.json()["items"]
    assert any(item["name"] == "mock" for item in items)


def test_estimate_image_generation() -> None:
    response = client.post(
        "/api/v1/generate/estimate",
        json={"type": "image", "mode": "text_to_image", "count": 4, "duration": 5},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["cost"] == 4
    assert body["selected_provider"] == "mock"


def test_generate_image_and_query_task() -> None:
    response = client.post(
        "/api/v1/generate/image",
        json={"prompt": "雨夜东京街头的橘猫", "mode": "text_to_image", "count": 1},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["results"][0]["type"] == "image"

    task_response = client.get(body["poll_url"])
    assert task_response.status_code == 200
    assert task_response.json()["id"] == body["task_id"]


def test_generate_video_and_query_task() -> None:
    response = client.post(
        "/api/v1/generate/video",
        json={"prompt": "赛博城市上空的飞鸟", "mode": "text_to_video", "duration": 5},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["results"][0]["type"] == "video"

    task_response = client.get(body["poll_url"])
    assert task_response.status_code == 200
    assert task_response.json()["progress"] == 100
