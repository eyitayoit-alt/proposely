#!/bin/bash

# Variables
DB_USER="appuser"
DB_PASS="2ndApril"
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
CREATE INDEX cvs_embedding_idx ON cvs USING diskann (embedding);
"

# Update and install prerequisites
echo "Updating system packages..."
sudo apt update -y

# Add PostgreSQL's official repository for PostgreSQL 16
echo "Adding PostgreSQL repository..."
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Install PostgreSQL 16 and extensions
echo "Installing PostgreSQL 16 and extensions..."
sudo apt update -y
sudo apt install -y postgresql-16 postgresql-contrib libpq-dev

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

# Install pgvector and pgai extensions
echo "Installing pgvector extension..."
sudo -u postgres psql -c "CREATE EXTENSION IF NOT EXISTS pgvector;"

echo "Installing pgai extension..."
sudo -u postgres psql -c "CREATE EXTENSION IF NOT EXISTS pgai;"

echo "Installing pgvector_scale extension..."
sudo -u postgres psql -c "CREATE EXTENSION IF NOT EXISTS pgvector_scale;"

# Create a new database user and set the password
echo "Creating database user '${DB_USER}'..."
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH LOGIN PASSWORD '${DB_PASS}';"

# Create a new database and grant privileges to the new user
echo "Creating database '${DB_NAME}'..."
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# Enable extensions on the new database
echo "Activating extensions on ${DB_NAME}..."
sudo -u postgres psql -d ${DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS pgvector;"
sudo -u postgres psql -d ${DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS pgai;"
sudo -u postgres psql -d ${DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS pgvector_scale;"

# Execute SQL to create a sample table
echo "Creating tables in the ${DB_NAME} database..."
sudo -u postgres psql -d ${DB_NAME} -c "${TABLE_SQL}"

echo "PostgreSQL 16, pgvector, pgai, and pgvector_scale setup is complete."
