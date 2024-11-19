#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Source environment variables from .env if not already set
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Run the pgdocker.sh script to set up the database (if needed)
echo "Running pgdocker.sh to set up the database..."
./pgdocker.sh || { echo "Failed to run pgdocker.sh"; exit 1; }

# Run any other setup commands if needed

# Start the main application (e.g., Streamlit)
echo "Starting the Streamlit app..."
streamlit run app.py 
