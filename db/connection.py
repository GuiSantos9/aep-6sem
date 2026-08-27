import os
from pymongo import MongoClient

# Lê a URL configurada no docker-compose.yml
mongo_uri = os.environ["MONGO_URI"]
client = MongoClient(mongo_uri)

db = client["meubanco"]