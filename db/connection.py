from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from os import environ
from pathlib import Path

from dotenv import dotenv_values
from fastapi import FastAPI, Request
from pymongo import MongoClient
from pymongo.database import Database


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

config = dotenv_values(ENV_PATH)


def obter_configuracao(nome: str) -> str:
    valor = environ.get(nome) or config.get(nome)

    if not valor:
        raise RuntimeError(
            f"A variável {nome} precisa estar configurada "
            "no ambiente ou no arquivo .env."
        )

    return valor


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    mongo_uri = obter_configuracao("MONGO_URI")
    db_name = obter_configuracao("DB_NAME")

    client = MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=5000,
    )

    # Verifica se o MongoDB realmente está acessível
    client.admin.command("ping")

    app.state.mongodb_client = client
    app.state.database = client[db_name]

    print("Conectado ao MongoDB!")

    try:
        yield
    finally:
        client.close()
        print("Conexão com MongoDB encerrada.")


def get_database(request: Request) -> Database:
    return request.app.state.database