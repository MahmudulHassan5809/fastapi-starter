#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Extract the database name, user, and password from DATABASE_URL
DB_NAME=$(echo $DATABASE_URL | sed -E 's/^.*\/([^?]+).*$/\1/')
DB_USER=$(echo $DATABASE_URL | sed -E 's/^.*\/\/([^:]+):.*$/\1/')
DB_PASSWORD=$(echo $DATABASE_URL | sed -E 's/^.*:([^@]+)@.*$/\1/')

# Run PostgreSQL commands as the postgres user
sudo -u postgres bash <<EOF
psql -c "DROP DATABASE IF EXISTS $DB_NAME;"
psql -c "CREATE DATABASE $DB_NAME;"
psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
EOF

echo "Database '$DB_NAME' and user '$DB_USER' setup completed."
echo "Using DATABASE_URL from .env: $DATABASE_URL"
