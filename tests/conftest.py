import mongomock
import pytest
from fastapi.testclient import TestClient

from app.main import app
from db.connection import criar_indices


@pytest.fixture
def client():
    mongodb_client = mongomock.MongoClient()
    database = mongodb_client.inospita_test
    criar_indices(database)

    app.state.mongodb_client = mongodb_client
    app.state.database = database
    with TestClient(app) as test_client:
        yield test_client

    mongodb_client.close()
    del app.state.mongodb_client
    del app.state.database

