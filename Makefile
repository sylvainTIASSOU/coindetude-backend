.PHONY: dev test lint format migrate revision shell

dev:
	poetry run fastapi dev app/main.py --host 0.0.0.0 --port 8008

test:
	poetry run pytest -v --cov=app

lint:
	poetry run ruff check .
	poetry run mypy app

format:
	poetry run ruff format .
	poetry run ruff check --fix .

migrate:
	poetry run alembic upgrade head

revision:
	poetry run alembic revision --autogenerate -m "$(m)"

shell:
	poetry run python
