
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys and DB credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
POSTGRES_DB = os.getenv("POSTGRES_DB")
HOST = os.getenv("HOST")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PORT = os.getenv("PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
