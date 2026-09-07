# Inóspita API

API REST para registro, consulta e acompanhamento de denúncias de arquitetura hostil em espaços urbanos.

---

## Objetivo

Permitir o registro e gerenciamento de ocorrências de arquitetura hostil (bancos divididos, espigões metálicos, barreiras físicas etc.), com classificação por tipo e prioridade.

---

## Como executar

### Com Docker (recomendado)

```bash
cp .env.example .env
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.  
Documentação interativa: `http://localhost:8000/docs`.

### Localmente

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
cp .env.example .env         # configure MONGO_URI e DB_NAME
uvicorn app.main:app --reload
```

### Testes

```bash
pytest tests/ -v
```

---

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `MONGO_USER` | Usuário do MongoDB (usado pelo Docker Compose) |
| `MONGO_PASSWORD` | Senha do MongoDB (usado pelo Docker Compose) |
| `MONGO_URI` | URI completa de conexão com o MongoDB |
| `DB_NAME` | Nome do banco de dados |

---

## Estrutura de pastas

```
aep-6sem/
├── app/
│   ├── main.py              # Ponto de entrada FastAPI
│   ├── exceptions.py        # Exceções de domínio
│   ├── entities/
│   │   └── denuncia.py      # TypedDict do documento MongoDB
│   ├── enums/
│   │   ├── prioridade.py
│   │   ├── status.py
│   │   └── tipo.py
│   ├── repositories/
│   │   └── denuncia_repository.py
│   ├── routers/
│   │   └── denuncia.py      # Endpoints REST
│   ├── schemas/
│   │   └── denuncia.py      # Modelos Pydantic (request/response)
│   └── services/
│       └── denuncia_service.py
├── db/
│   └── connection.py        # Conexão MongoDB + lifespan
├── tests/
│   ├── conftest.py
│   └── test_denuncias.py
├── .env.example
├── docker-compose.yaml
├── Dockerfile
└── requirements.txt
```
