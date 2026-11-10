from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_health_returns_ok():
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "development"}


def test_unknown_route_returns_404():
    client = TestClient(create_app())
    assert client.get("/nope").status_code == 404


def test_health_rejects_non_get():
    client = TestClient(create_app())
    assert client.post("/health").status_code == 405


def test_settings_read_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    settings = Settings()
    assert settings.app_env == "test"
    assert settings.log_level == "WARNING"


def test_settings_reject_invalid_environment(monkeypatch):
    import pydantic
    import pytest

    monkeypatch.setenv("APP_ENV", "staging-ish")
    with pytest.raises(pydantic.ValidationError):
        Settings()


def test_docs_disabled_in_production(monkeypatch):
    from app import config

    monkeypatch.setenv("APP_ENV", "production")
    config.get_settings.cache_clear()
    try:
        client = TestClient(create_app())
        assert client.get("/health").json()["environment"] == "production"
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404
    finally:
        config.get_settings.cache_clear()
