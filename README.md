# Web API FastAPI Template

A template repository for creating an async web API using FastAPI, Pydantic, and SQLAlchemy 2.x.

## Local development

At project root, perform the following.

1. Use python 3.12
    ```console
    $ pyenv install 3.12
    $ pyenv local 3.12
    ```
2. Install poetry
    ```console
    $ brew install poetry
    ```
3. Set up virtual environment
    ```console
    $ poetry env use 3.12
    $ poetry install
    ```
4. Create a personal config file and set `API_KEY` (it is git-ignored, so no sensitive information ends up in the codebase)
    ```console
    $ make local
    ```
5. Run the server (tables are created on startup)
    ```console
    $ make serve
    ```
6. Call the API, or open the interactive docs at <http://127.0.0.1:8000/docs> (use **Authorize** to set the key)
    ```console
    $ curl -H "X-API-Key: change-me" http://127.0.0.1:8000/api/v1/widgets
    ```

Run the tests with `make test` and format the code with `make lint`.

## Layout

| Path | Purpose |
| --- | --- |
| `web_api/` | App entrypoint (`main.py`) and settings (`config.py`) |
| `api/` | HTTP layer: routers under `api/v1/` and shared dependencies (auth, db session) in `deps.py` |
| `core/` | Business logic: `services/`, `dtos/` (Pydantic), `clients/` (outbound HTTP), `models.py` and `db.py` (SQLAlchemy) |
| `common_libs/` | Shared helpers, e.g. colored logging for local runs |
| `tests/` | Async tests against the app with an isolated sqlite database |

## Configuration

Settings come from environment variables, or from a `.env` file, and are defined in `web_api/config.py`.

| Variable | Default | Notes |
| --- | --- | --- |
| `ENVIRONMENT` | `local` | `local`, `staging`, `prod`, ... Colored logging is used only for `local` |
| `API_KEY` | unset | Required in the `X-API-Key` header for `/api/v1/*`; requests are rejected while unset |
| `DATABASE_URL` | `sqlite+aiosqlite:///./app.db` | Any async SQLAlchemy URL, e.g. `postgresql+asyncpg://...` (add the driver) |
| `LOG_LEVEL` | `INFO` | |
| `SAMPLE_API_BASE_URL` | `https://api.sampleapis.com` | Upstream used by the sample TV show client |

## Notes

- Handlers are `async def` end to end (async SQLAlchemy session, `httpx.AsyncClient`). Avoid blocking calls inside them, as they stall the event loop.
- Tables are created on startup for convenience. Add a migration tool such as Alembic once the schema starts to change.
