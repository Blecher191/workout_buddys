# Backend

Python 3.13+ and FastAPI. Currently provides a health endpoint only; authentication, data and
workout routes come in later tasks (see [../docs/project-plan.md](../docs/project-plan.md)).

## Setup

From the `backend` directory.

Windows (PowerShell):

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
```

macOS / Linux:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

In PyCharm, set the project interpreter to the `.venv` you just created.

## Run

```sh
uvicorn app.main:app --reload
```

Then open <http://127.0.0.1:8000/health>. Expected response:
`{"status":"ok","environment":"development"}`. Interactive docs are at `/docs` unless
`APP_ENV=production`.

## Check

```sh
ruff check .
ruff format --check .
pytest
```

These same commands run in CI (`.github/workflows/backend.yml`).

## Configuration

Environment variables, or a local `.env` (ignored by git). See `.env.example`; only placeholder
values belong in that file.

| Variable | Values | Default |
|---|---|---|
| `APP_ENV` | `development`, `test`, `production` | `development` |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |

## Dependencies

Direct dependencies are declared in `pyproject.toml`. `requirements.txt` pins the full resolved
runtime set and `requirements-dev.txt` adds pinned test and lint tools. To refresh the pins,
install the `pyproject.toml` dependencies into a clean virtual environment, run
`pip freeze --all`, and update both files (keeping dev-only packages in `requirements-dev.txt`).
