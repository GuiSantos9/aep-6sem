from os import environ
from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

# Lê a URL configurada no docker-compose.yml
mongo_uri = environ["MONGO_URI"]

config = dotenv_values(".env")
app = FastAPI()


@app.on_event("startup")
def iniciar_cliente_db():
    app.mongodb_client = MongoClient(mongo_uri)
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def finalizar_cliente_db():
    app.mongodb_client.close()
