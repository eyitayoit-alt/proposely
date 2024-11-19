# Use Python 3.12 as the base image for the Proposely app
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pgdocker.sh and make it executable

COPY init.sql /docker-entrypoint-initdb.d/
# Copy the entire application code into the container

COPY pgdocker.sh .
RUN chmod +x pgdocker.sh

RUN ./pgdocker.sh || { echo "pgdocker.sh failed"; exit 1; }

COPY . .


# Expose the Streamlit app's default port
EXPOSE 8501

# Entry point script to handle multiple commands
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
