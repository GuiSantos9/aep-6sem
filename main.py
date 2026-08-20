from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI(
    title="API de teste",
    version= "1.0.0"
)

class Item(BaseModel):
    nome: str
    preco: float 
    em_estoque: bool = True

# rota inicial
@app.get("/")
def home():
    return {"mensagem": "API funcionando com sucesso"}

# rota com parâmetro na url 
@app.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int):
    return {"usuario_id": usuario_id, "status": "ativo"}

# rota para receber dados
@app.post("/itens/")
def criar_itens(item: Item):
    return {"mensagem": "Item recebido com sucesso", "dados": item}