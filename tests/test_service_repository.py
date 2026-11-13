"""Casos defensivos do repositório e falhas entre consulta e escrita."""
from unittest.mock import create_autospec

import mongomock
import pytest
from bson import ObjectId

from app.exceptions import NotFoundError
from app.repositories.report_repository import DenunciaRepository, converter_object_id
from app.services.report_service import DenunciaService
from app.schemas.report import DenunciaUpdate


def test_conversao_object_id():
    identifier = ObjectId()
    assert converter_object_id(str(identifier)) == identifier
    assert converter_object_id('invalido') is None


@pytest.mark.parametrize('method', ['get_by_id', 'update', 'delete'])
@pytest.mark.parametrize('identifier', ['invalido', str(ObjectId())])
def test_repositorio_nao_cria_registro_ausente(method, identifier):
    database = mongomock.MongoClient().test
    repository = DenunciaRepository(database)
    args = (identifier, {'titulo': 'Novo título'}) if method == 'update' else (identifier,)
    result = getattr(repository, method)(*args)
    assert result is False if method == 'delete' else result is None
    assert database.denuncias.count_documents({}) == 0


@pytest.mark.parametrize('method', ['update', 'delete'])
def test_servico_registro_removido_entre_consulta_e_escrita(method):
    repository = create_autospec(DenunciaRepository, instance=True)
    repository.get_by_id.return_value = {'titulo': 'Denúncia existente'}
    repository.update.return_value = None
    repository.delete.return_value = False
    service = DenunciaService(repository)
    identifier = str(ObjectId())
    args = (identifier, DenunciaUpdate(titulo='Novo título')) if method == 'update' else (identifier,)
    with pytest.raises(NotFoundError, match='não encontrada'):
        getattr(service, method)(*args)
    repository.get_by_id.assert_called_once_with(identifier)
    if method == 'update':
        repository.update.assert_called_once_with(identifier, {'titulo': 'Novo título'})
    else:
        repository.delete.assert_called_once_with(identifier)
