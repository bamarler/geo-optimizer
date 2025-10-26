from pymongo import MongoClient
from datetime import datetime
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["chatgpt_geo_testing"]
        self.results = self.db["test_results"]
    
    def insert_test_result(self, data: Dict) -> str:
        """Insert test result and return inserted ID."""
        data["timestamp"] = datetime.utcnow()
        result = self.results.insert_one(data)
        return str(result.inserted_id)
    
    def close(self):
        self.client.close()