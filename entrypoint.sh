#!/bin/bash

# Check the APP_MODE environment variable to decide which command to run
if [ "$APP_MODE" = "streamlit" ]; then
    echo "Starting Streamlit app..."
    streamlit run app.py
elif [ "$APP_MODE" = "cli" ]; then
    echo "Running CLI app..."
    python3 cli.py
else
    echo "APP_MODE not set or unrecognized. Please set APP_MODE to 'streamlit' or 'cli'."
    exit 1
fi

