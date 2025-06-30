.PHONY: reset-db deploy reset-migrations

SHELL := /bin/bash

reset-db:
	@export $$(grep -v '^#' .env | xargs) && \
	DB_NAME=$$(echo $$DATABASE_URL | sed -E 's|.*/([^/?]+).*|\1|') && \
	DB_USER=$$(echo $$DATABASE_URL | sed -E 's|.*://([^:]+):.*|\1|') && \
	sudo -u postgres psql -c "DROP DATABASE IF EXISTS $$DB_NAME;" && \
	sudo -u postgres psql -c "CREATE DATABASE $$DB_NAME;" && \
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $$DB_NAME TO $$DB_USER;" && \
	echo "Postgres User '$$DB_USER' and database '$$DB_NAME' reset successfully."



reset-migrations:
	@export $$(grep -v '^#' .env | xargs) && \
	source .venv/bin/activate && \
	rm -rf alembic/versions/* && \
	alembic revision --autogenerate -m "Initial Migrations" && \
	alembic upgrade head && \
	echo "Migrations reset successfully."
