from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="API de teste",
    version="1.0.0"
)

# rota inicial


@app.get("/")
def home():
    return {"mensagem": "API funcionando com sucesso"}
