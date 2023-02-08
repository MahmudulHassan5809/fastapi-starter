#! /usr/bin/env bash


# Let the DB start
python src/db/db_check.py


# Run migrations
alembic upgrade head

# Create initial data in DB
python src/seeders/create_super_user.py