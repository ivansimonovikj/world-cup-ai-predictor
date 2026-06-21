from pymongo import MongoClient
from config import Config
import certifi

# 1. Initialize MongoDB Client with the certifi fix
client = MongoClient(Config.MONGO_URI, tlsCAFile=certifi.where())

# 2. Target the HISTORICAL database for the AI model
db = client["world_cup_predictor"]

# 3. Target the HISTORICAL collection for training
matches_col = db["matches"]
predictions_col = db["predictions"]

def check_db_connection():
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

if __name__ == "__main__":
    check_db_connection()