import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    API_KEY = os.getenv("API_FOOTBALL_KEY")
    API_URL = "https://v3.football.api-sports.io"

    if not API_KEY:
        raise ValueError("CRITICAL: API_FOOTBALL_KEY is missing from your .env file!")