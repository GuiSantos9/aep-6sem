# Inóspita API

Registra, consulta e acompanha denúncias de arquitetura hostil (bancos com divisórias, espigões, aspersores etc.). Stack: Python 3.12, FastAPI, MongoDB, Docker, pytest. Front em HTML/CSS/JS.

## 1. Executar (MongoDB + API)
```bash
copy .env.example .env      # Linux/macOS: cp .env.example .env
docker compose up --build   # API: http://localhost:8000/docs | health: /health
docker compose down         # encerrar (o volume mongo_data preserva os dados)
```
Front (outro terminal): `python -m http.server 5500 --bind 127.0.0.1 --directory front` → http://localhost:5500 (quadro de tarefas: `/board.html`). A API deve estar em `BASE_URL` (`front/app.js`).

## 2. Testar (não exige Docker nem MongoDB: usa mongomock)
```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest   # Linux/macOS: .venv/bin/python
```
Resultado verificado: **95 testes aprovados, 99,03% de cobertura** de `app/` e `db/` (mínimo exigido: 70%, configurado em `pytest.ini`). Gera `coverage.xml` e `htmlcov/`. O JS do front não é medido.

## 3. Banco NoSQL (MongoDB, 2 coleções)
```text
locais                        denuncias
{ _id, nome, bairro,    1 ◄─N { _id, titulo, descricao, tipo, prioridade, status,
  cidade, uf, referencia,       logradouro, numero, bairro, cidade, uf, cep,
  criado_em }                   evidencias: [url],
                                local_id  → locais._id   (relacionamento),
                                historico: [{status_anterior, status_novo,
                                             observacao, data}]  (subdocumentos),
                                criado_em, atualizado_em }
```
Local inexistente → 422; excluir local com denúncias → 409. Índices: `tipo`, `prioridade`, `criado_em`, `local_id`, `locais.nome`. Na inicialização há seed (3 locais e 3 denúncias) se as coleções estiverem vazias.

## 4. Rotas
`POST/GET /denuncias`, `GET/PATCH/DELETE /denuncias/{id}` (filtros: `tipo`, `prioridade`, `local_id`, `limit`, `offset`); `POST/GET /locais`, `GET/DELETE /locais/{id}`, `GET /locais/{id}/denuncias`. `PATCH` com `status` (+ `observacao`) acrescenta item ao `historico`.

## 5. Fluxo e domínio
Status: `registrada` → `em_analise` → `encaminhada` → `resolvida` | `arquivada`. Tipos: `banco_dividido`, `espigao_metalico`, `inclinacao_de_superficie`, `retirada_de_assento`, `barreira_fisica`, `emissao_sonora`, `aspersor_de_agua`, `outro`. Prioridades: baixa, media, alta, urgente.

## 6. Estrutura
`app/` (routers → services → repositories, + schemas, entities, enums, exceptions) · `db/` (conexão, índices, seed) · `front/` · `tests/` · `Dockerfile`, `docker-compose.yaml`, `.env.example` (variáveis: `MONGO_USER`, `MONGO_PASSWORD`, `DB_NAME`, `MONGO_URI`, `APP_NAME`).
