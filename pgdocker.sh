#!/bin/bash
source .env

# Database connection details
DB_USER="${POSTGRES_USER}"
DB_PASS="${POSTGRES_PASSWORD}"
DB_NAME="${POSTGRES_DB}"
DB_HOST="timescaledb"  # Use the service name in Docker Compose

echo "Creating database user '${DB_USER}'..."
PGPASSWORD="${DB_PASS}" psql -h "${DB_HOST}" -U postgres -c "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${DB_USER}') THEN CREATE USER ${DB_USER} WITH LOGIN PASSWORD '${DB_PASS}'; END IF; END \$\$;"

echo "Creating database '${DB_NAME}'..."
PGPASSWORD="${DB_PASS}" psql -h "${DB_HOST}" -U postgres -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

echo "Database setup complete."
