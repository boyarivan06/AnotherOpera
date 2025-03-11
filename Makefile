install:
	poetry install
build:
	poetry build
run:
	poetry run project
lint:
	poetry run ruff check --fix
lab:
	poetry run lab