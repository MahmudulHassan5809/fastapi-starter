#! /usr/bin/env bash


# Let the DB start
python src/db/db_check.py


# Run migrations
alembic upgrade head

# Create initial data in DB
# python ./app/initial_data.py