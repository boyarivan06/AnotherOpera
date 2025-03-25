install:
	poetry install
build:
	poetry build
	@if [test -f .env = '']; then \
	    cat .env-example > .env; \
	fi

run:
	poetry run bot | poetry run app
bot:
	poetry run bot
lint:
	isort .
	black .
	poetry run ruff check --fix
app:
	poetry run app
