#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Extract the database name, user, and password from DATABASE_URL
DB_NAME=$(echo $TEST_DATABASE_URL | sed -E 's/^.*\/([^?]+).*$/\1/')
DB_USER=$(echo $TEST_DATABASE_URL | sed -E 's/^.*\/\/([^:]+):.*$/\1/')
DB_PASSWORD=$(echo $TEST_DATABASE_URL | sed -E 's/^.*:([^@]+)@.*$/\1/')

# Run PostgreSQL commands as the postgres user
sudo -u postgres bash <<EOF
psql -c "DROP DATABASE IF EXISTS $DB_NAME;"
psql -c "CREATE DATABASE $DB_NAME;"
psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
EOF

echo "Database '$DB_NAME' and user '$DB_USER' setup completed."
echo "Using TEST_DATABASE_URL from .env: $TEST_DATABASE_URL"
