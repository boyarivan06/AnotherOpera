install:
	poetry install
build:
	poetry build
run:
	poetry run bot | poetry run project
bot:
	poetry run bot
lint:
	poetry run ruff check --fix
lab:
	poetry run lab
project:
	poetry run project
