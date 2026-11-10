import os

import pytest

from app import config

# Settings the application reads. Test runs must not depend on whatever the developer's shell
# or CI runner happens to export for them, valid or not.
_ISOLATED_ENV = {"APP_ENV": "development", "LOG_LEVEL": "INFO"}
_saved_env: dict[str, str | None] = {}


def pytest_configure(config):
    """Sanitize inherited settings before test collection.

    `app.main` builds the application, and so validates settings, when it is first imported, and
    test modules import it during collection. A fixture runs too late for that, so a bad inherited
    APP_ENV or LOG_LEVEL would otherwise abort collection. Real application startup is not
    affected: this only changes the environment of the pytest process.
    """
    for name, value in _ISOLATED_ENV.items():
        _saved_env[name] = os.environ.get(name)
        os.environ[name] = value


def pytest_unconfigure(config):
    for name, original in _saved_env.items():
        if original is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = original
    _saved_env.clear()


@pytest.fixture(autouse=True)
def _hermetic_settings(monkeypatch):
    """Per test: known-good settings and an empty settings cache, undone afterwards."""
    for name, value in _ISOLATED_ENV.items():
        monkeypatch.setenv(name, value)
    config.get_settings.cache_clear()
    yield
    config.get_settings.cache_clear()
