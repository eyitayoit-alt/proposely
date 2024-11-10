# Use Python 3.12 as the base image for the Proposely app
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pgdocker.sh ./app
RUN chmod +x /app/pgdocker.sh
RUN /app/pgdocker.sh

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
# Copy the entire application code into the container
COPY . .

# Expose the Streamlit app's default port
EXPOSE 8501

# Define environment variables (these will be set in the docker-compose.yml file)
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
ENV OLLAMA_API_KEY=$OLLAMA_API_KEY

# Command to run the Streamlit app
CMD ["/app/entrypoint.sh"]
