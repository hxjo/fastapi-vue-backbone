#!/bin/bash
set -e

# PostgreSQL service startup delay
sleep 10

# Function to check if the database exists
check_database() {
    psql -lqt | cut -d \| -f 1 | grep -qw $FGA_DB_NAME
}

# Function to create the database if it does not exist
create_database() {
    echo "Creating database: $FGA_DB_NAME"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE DATABASE $FGA_DB_NAME;
EOSQL
}

# Main execution
if ! check_database; then
    create_database
else
    echo "Database $FGA_DB_NAME already exists"
fi

# Call the original entrypoint script to ensure normal PostgreSQL startup
exec docker-entrypoint.sh postgres
