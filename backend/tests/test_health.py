from fastapi.testclient import TestClient


def test_health_ok(api_client: TestClient) -> None:
    response = api_client.get("/health")

    assert response.status_code == 200
    json_body = response.json()
    assert json_body["status"] == "ok"
    assert json_body["database"] == "connected"
