"""Regression tests: test isolation from inherited settings, and startup validation preserved.

The first group runs pytest in a child process so that collection itself, which is where the
original failure happened, is exercised under hostile inherited configuration. The second group
proves the isolation lives in the test setup only: the application still rejects invalid settings.
"""

import os
import subprocess
import sys
from pathlib import Path

import pydantic
import pytest

from app.config import Settings

BACKEND_DIR = Path(__file__).resolve().parents[1]
# A different test module, so the child process cannot recurse into this file.
TARGET_TESTS = BACKEND_DIR / "tests" / "test_health.py"


def run_in_child(args: list[str], env_overrides: dict[str, str], cwd: Path = BACKEND_DIR):
    env = {**os.environ, **env_overrides}
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.mark.parametrize(
    "inherited",
    [
        {"APP_ENV": "bogus", "LOG_LEVEL": "nope"},
        {"APP_ENV": "", "LOG_LEVEL": ""},
        # Valid but different from what the tests assume.
        {"APP_ENV": "production", "LOG_LEVEL": "DEBUG"},
    ],
    ids=["both-invalid", "empty", "valid-but-different"],
)
def test_suite_collects_and_passes_with_inherited_settings(inherited):
    result = run_in_child(
        ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-W", "error", str(TARGET_TESTS)],
        inherited,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "passed" in result.stdout


def test_suite_ignores_invalid_values_in_a_local_dotenv_file(tmp_path):
    (tmp_path / ".env").write_text("APP_ENV=bogus\nLOG_LEVEL=nope\n")
    result = run_in_child(
        ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-W", "error", str(TARGET_TESTS)],
        {"APP_ENV": "bogus", "LOG_LEVEL": "nope"},
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    ("name", "value"),
    [("APP_ENV", "bogus"), ("APP_ENV", ""), ("LOG_LEVEL", "nope"), ("LOG_LEVEL", "")],
)
def test_settings_still_reject_invalid_values(monkeypatch, name, value):
    monkeypatch.setenv(name, value)
    with pytest.raises(pydantic.ValidationError) as excinfo:
        Settings()
    assert name.lower() in str(excinfo.value)


@pytest.mark.parametrize(
    ("name", "value"),
    [("APP_ENV", "bogus"), ("LOG_LEVEL", "nope")],
)
def test_application_startup_fails_fast_on_invalid_settings(name, value):
    # Plain interpreter, no pytest and so no conftest: this is what uvicorn would do.
    result = run_in_child(["-c", "import app.main"], {name: value})
    assert result.returncode != 0
    assert "ValidationError" in result.stderr
    assert name.lower() in result.stderr


def test_application_startup_succeeds_with_valid_settings():
    result = run_in_child(["-c", "import app.main"], {"APP_ENV": "test", "LOG_LEVEL": "WARNING"})
    assert result.returncode == 0, result.stderr
