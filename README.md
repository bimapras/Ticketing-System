# TicketSystem

This repository is a small FastAPI-based ticketing application that I built as part of assignment DataExpert FreeBootCamp and also my journey to learn software engineering. It is a practical project that combines backend development, templates, database access, and environment-based configuration in one place.

## Tech stack

- Python 3.12
- FastAPI for the API and web app
- Uvicorn as the ASGI server
- Jinja2 templates for the frontend rendering
- psycopg2 and SQLAlchemy for database access
- python-dotenv for environment variables
- uv for dependency and environment management

## Project structure

- [app.py](app.py) - creates the FastAPI app and serves the homepage
- [routes/ticket.py](routes/ticket.py) - ticket-related API endpoints
- [schema/](schema/) - request/response models
- [templates/](templates/) - HTML templates used by the app
- [lakebase.py](lakebase.py) and [local_lakebase.py](local_lakebase.py) - database connection helpers
- [pyproject.toml](pyproject.toml) - project dependencies and Python version
- [uv.lock](uv.lock) - locked dependencies for reproducible installs

## Prerequisites

Before running this project, make sure you have:

- Python 3.12 installed
- uv installed on your machine

If uv is not installed yet, install it first:

- Official installation guide: https://docs.astral.sh/uv/getting-started/installation/

## Install and sync the environment with uv

This project uses uv to manage dependencies and the virtual environment.

From the repository root, run:

```bash
uv venv --python 3.12
uv sync
```

That command will:

- create virtual environment with Python 3.12
- install dependencies from [pyproject.toml](pyproject.toml)
- sync everything based on [uv.lock](uv.lock)

## Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

## Configure environment variables

This project uses a database connection string to talk to Lakebase/PostgreSQL from databricks.

Create a `.env` file in the project root and define the connection URL:

```env
LAKEBASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

If you are using the local helper in [local_lakebase.py](local_lakebase.py), this variable is the one that will be read.

## Run the app

You can start the server with:

```bash
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

## Useful uv commands

- Sync dependencies:

```bash
uv sync
```

- Run a command inside the project environment:

```bash
uv run <command>
```

- Update the lockfile after changing dependencies:

```bash
uv lock
```

## Notes for this learning project

This repository is intentionally simple and educational. It is a good example of:

- building a small web app end to end
- structuring a Python project with routes and schemas
- connecting to a real database
- using modern tooling like uv

As I keep learning, I can improve this project by adding better tests, cleaner architecture, authentication, and deployment practices.
