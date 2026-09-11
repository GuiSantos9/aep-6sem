"""Configuração, seed e ciclo de conexão, sem acesso à rede."""
import asyncio
from copy import deepcopy
from unittest.mock import Mock

import mongomock
import pytest
from fastapi import FastAPI

from db import connection
from db.seed import SEED, seed_denuncias
from app.schemas.denuncia import DenunciaResponse


@pytest.mark.parametrize('environment,config,expected', [
    ('ambiente', 'arquivo', 'ambiente'), (None, 'arquivo', 'arquivo'),
    ('', 'arquivo', 'arquivo'),
])
def test_configuracao(monkeypatch, environment, config, expected):
    monkeypatch.setattr(connection, 'config', {'DB_NAME': config})
    monkeypatch.delenv('DB_NAME', raising=False)
    if environment is not None:
        monkeypatch.setenv('DB_NAME', environment)
    assert connection.obter_configuracao('DB_NAME') == expected


def test_configuracao_ausente(monkeypatch):
    monkeypatch.setattr(connection, 'config', {})
    monkeypatch.delenv('DB_NAME', raising=False)
    with pytest.raises(RuntimeError, match='DB_NAME precisa estar configurada'):
        connection.obter_configuracao('DB_NAME')


def test_indices_e_seed_idempotente():
    database = mongomock.MongoClient().test
    connection.criar_indices(database)
    keys = [item['key'] for item in database.denuncias.index_information().values()]
    assert [('tipo', 1)] in keys
    assert [('prioridade', 1)] in keys
    assert [('criado_em', -1)] in keys
    seed_denuncias(database)
    documentos = list(database.denuncias.find())
    assert len(documentos) == len(SEED)
    assert {d['titulo'] for d in documentos} == {d['titulo'] for d in SEED}
    for documento in documentos:
        DenunciaResponse.model_validate(documento)
    seed_denuncias(database)
    assert list(database.denuncias.find()) == documentos


def test_seed_preserva_banco_existente():
    database = mongomock.MongoClient().test
    documento = deepcopy(SEED[0])
    documento['titulo'] = 'Denúncia do usuário'
    database.denuncias.insert_one(documento)
    antes = list(database.denuncias.find())
    seed_denuncias(database)
    assert list(database.denuncias.find()) == antes
    assert antes[0]['titulo'] == 'Denúncia do usuário'


@pytest.mark.parametrize('erro_no_corpo', [False, True])
def test_lifespan_inicializa_e_fecha(monkeypatch, erro_no_corpo):
    database = mongomock.MongoClient().test
    mongo = Mock()
    mongo.__getitem__ = Mock(return_value=database)
    factory = Mock(return_value=mongo)
    monkeypatch.setattr(connection, 'MongoClient', factory)
    monkeypatch.setenv('MONGO_URI', 'mongodb://localhost:27017')
    monkeypatch.setenv('DB_NAME', 'inospita_test')
    app = FastAPI()

    async def executar():
        async with connection.lifespan(app):
            assert app.state.database is database
            assert database.denuncias.count_documents({}) == len(SEED)
            mongo.admin.command.assert_called_once_with('ping')
            if erro_no_corpo:
                raise ValueError('falha durante uso')
    if erro_no_corpo:
        with pytest.raises(ValueError, match='falha durante uso'):
            asyncio.run(executar())
    else:
        asyncio.run(executar())
    factory.assert_called_once_with('mongodb://localhost:27017', serverSelectionTimeoutMS=5000)
    mongo.close.assert_called_once()
