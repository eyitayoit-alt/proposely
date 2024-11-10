#!/bin/bash

# Variables
DB_USER="proposelyuser"
DB_PASS="proposely"
DB_NAME="proposely"

TABLE_SQL="
-- Create necessary extensions if not already done
CREATE EXTENSION IF NOT EXISTS ai CASCADE;
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;

-- Create table to store CV content and embeddings
CREATE TABLE IF NOT EXISTS cvs (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    fullname TEXT NOT NULL UNIQUE,
    metadata JSONB,
    embedding VECTOR(768)
);

-- Create indexes for efficient similarity search
CREATE INDEX IF NOT EXISTS cvs_embedding_idx ON cvs USING diskann (embedding);
"


# Start PostgreSQL service
echo "Starting PostgreSQL service..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Check PostgreSQL status
if sudo systemctl is-active --quiet postgresql; then
  echo "PostgreSQL is running."
else
  echo "Failed to start PostgreSQL service. Exiting."
  exit 1
fi


# Create a new database user and set the password
echo "Creating database user '${DB_USER}'..."
sudo -u postgres psql -c "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${DB_USER}') THEN CREATE USER ${DB_USER} WITH LOGIN PASSWORD '${DB_PASS}'; END IF; END \$\$;"

# Create a new database and grant privileges to the new user
echo "Creating database '${DB_NAME}'..."
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"


# Execute SQL to create the table and index
echo "Creating tables and indexes in the ${DB_NAME} database..."
sudo -u postgres psql -d ${DB_NAME} -c "${TABLE_SQL}"

echo "PostgreSQL 16, pgvector, pgai, and pgvector_scale setup is complete."
