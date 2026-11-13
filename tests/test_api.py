"""Integração HTTP com rotas, schemas, serviços e repositório reais; banco simulado."""
from datetime import datetime, timedelta, timezone
import pytest
from bson import ObjectId
from tests.test_reports import DENUNCIA_VALIDA, criar_denuncia


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
    assert response.json()['app']


def test_consulta_e_exclusao(client):
    criada = criar_denuncia(client)
    url = '/denuncias/' + criada['id']
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == criada
    assert criada['titulo'] == DENUNCIA_VALIDA['titulo']
    assert criada['evidencias'] == DENUNCIA_VALIDA['evidencias']
    assert datetime.fromisoformat(criada['criado_em'].replace('Z', '+00:00'))
    response = client.delete(url)
    assert response.status_code == 204
    assert response.content == b''
    assert client.get('/denuncias').json()['total'] == 0


@pytest.mark.parametrize('method', ['get', 'patch', 'delete'])
@pytest.mark.parametrize('identifier', ['id-invalido', str(ObjectId())])
def test_inexistente(client, method, identifier):
    kwargs = {'json': {'titulo': 'Novo título'}} if method == 'patch' else {}
    response = getattr(client, method)('/denuncias/' + identifier, **kwargs)
    assert response.status_code == 404
    assert 'não encontrada' in response.json()['detail']


@pytest.mark.parametrize('field,value', [
    ('titulo', 'abcd'), ('titulo', 'x' * 121), ('descricao', 'curta'),
    ('descricao', 'x' * 5001), ('titulo', '     '), ('tipo', 'invalido'),
    ('prioridade', 'invalida'), ('uf', 'PAR'), ('cep', '123'),
    ('evidencias', ['arquivo-local']), ('evidencias', ['https://example.com'] * 11),
    ('logradouro', 'ab'), ('bairro', 'a'), ('cidade', 'a'),
])
@pytest.mark.parametrize('method', ['post', 'patch'])
def test_validacao_campos(client, field, value, method):
    if method == 'post':
        url, payload = '/denuncias', {**DENUNCIA_VALIDA, field: value}
    else:
        criada = criar_denuncia(client)
        url, payload = '/denuncias/' + criada['id'], {field: value}
    response = getattr(client, method)(url, json=payload)
    assert response.status_code == 422
    if method == 'post':
        assert client.get('/denuncias').json()['total'] == 0
    else:
        assert client.get(url).json() == criada


@pytest.mark.parametrize('field', ['titulo', 'descricao', 'tipo', 'logradouro', 'bairro', 'cidade', 'uf'])
def test_cadastro_exige_campos(client, field):
    payload = DENUNCIA_VALIDA.copy()
    del payload[field]
    assert client.post('/denuncias', json=payload).status_code == 422


@pytest.mark.parametrize('payload', [{}, *[{field: None} for field in [
    'titulo', 'descricao', 'tipo', 'prioridade', 'status', 'logradouro',
    'bairro', 'cidade', 'uf', 'evidencias']], {'status': 'invalido'}])
def test_patch_rejeita_vazio_e_nulos(client, payload):
    criada = criar_denuncia(client)
    url = '/denuncias/' + criada['id']
    assert client.patch(url, json=payload).status_code == 422
    assert client.get(url).json() == criada


def test_defaults_normalizacao_atualizacao_parcial(client):
    payload = {**DENUNCIA_VALIDA, 'titulo': '  Título válido  ', 'cidade': '  Maringá  '}
    del payload['prioridade']
    del payload['evidencias']
    response = client.post('/denuncias', json=payload)
    assert response.status_code == 201
    criada = response.json()
    assert criada['titulo'] == 'Título válido'
    assert criada['cidade'] == 'Maringá'
    assert criada['prioridade'] == 'media'
    assert criada['evidencias'] == []
    url = '/denuncias/' + criada['id']
    response = client.patch(url, json={'titulo': '  Título alterado  ', 'uf': 'sp', 'numero': None, 'cep': None})
    assert response.status_code == 200
    atual = response.json()
    assert atual == {**criada, 'titulo': 'Título alterado', 'uf': 'SP', 'numero': None, 'cep': None}
    assert client.get(url).json() == atual


@pytest.mark.parametrize('status', ['registrada', 'em_analise', 'encaminhada', 'resolvida', 'arquivada'])
def test_status(client, status):
    criada = criar_denuncia(client)
    url = '/denuncias/' + criada['id']
    assert client.patch(url, json={'status': status}).status_code == 200
    assert client.get(url).json()['status'] == status


def test_filtros_ordenacao_paginacao(client):
    ids = []
    for tipo, prioridade in [('outro', 'alta'), ('banco_dividido', 'alta'), ('banco_dividido', 'baixa')]:
        response = client.post('/denuncias', json={**DENUNCIA_VALIDA, 'tipo': tipo, 'prioridade': prioridade})
        assert response.status_code == 201
        ids.append(response.json()['id'])
    # Datas controladas: o teste não depende da velocidade do relógio.
    for i, identifier in enumerate(ids):
        client.app.state.database.denuncias.update_one({'_id': ObjectId(identifier)}, {'$set': {'criado_em': datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=i)}})
    response = client.get('/denuncias?limit=1&offset=1')
    assert response.status_code == 200
    body = response.json()
    assert (body['total'], body['limit'], body['offset']) == (3, 1, 1)
    assert [item['id'] for item in body['items']] == [ids[1]]
    body = client.get('/denuncias?tipo=banco_dividido').json()
    assert body['total'] == 2
    assert [item['id'] for item in body['items']] == [ids[2], ids[1]]
    body = client.get('/denuncias?tipo=banco_dividido&prioridade=alta').json()
    assert body['total'] == 1
    assert body['items'][0]['id'] == ids[1]
    assert client.get('/denuncias?prioridade=urgente').json()['items'] == []
    body = client.get('/denuncias?offset=99').json()
    assert body['items'] == [] and body['total'] == 3


@pytest.mark.parametrize('query', ['limit=0', 'limit=101', 'offset=-1', 'limit=abc', 'tipo=invalido', 'prioridade=invalida'])
def test_query_invalida(client, query):
    assert client.get('/denuncias?' + query).status_code == 422


def test_lista_vazia(client):
    assert client.get('/denuncias').json() == {'items': [], 'total': 0, 'limit': 20, 'offset': 0}
