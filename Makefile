serve:
	poetry run uvicorn web_api.main:app --reload

test:
	poetry run pytest

lint:
	poetry run black .

local:
	cp -n .env.example .env
