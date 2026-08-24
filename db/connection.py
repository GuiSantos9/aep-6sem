import os
from pymongo import MongoClient

# Lê a URL configurada no docker-compose.yml
mongo_uri = os.getenv("MONGO_URI", "mongodb://root:senha123@mongodb:27017/meubanco?authSource=admin")
client = MongoClient(mongo_uri)

db = client["meubanco"]