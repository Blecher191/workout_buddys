import pytest

from app import config


@pytest.fixture(autouse=True)
def _hermetic_settings(monkeypatch):
    """Keep tests independent of the developer's shell environment and local .env file."""
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    config.get_settings.cache_clear()
    yield
    config.get_settings.cache_clear()
