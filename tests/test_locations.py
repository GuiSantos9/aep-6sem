"""Segunda entrega: múltiplas coleções, relacionamento e subdocumentos."""
from bson import ObjectId

LOCAL = {'nome': 'Praça Central', 'bairro': 'Centro', 'cidade': 'Maringá', 'uf': 'pr'}
DENUNCIA = {
    'titulo': 'Banco com divisória',
    'descricao': 'Banco com barras que impedem deitar.',
    'tipo': 'banco_dividido',
    'logradouro': 'Rua A',
    'bairro': 'Centro',
    'cidade': 'Maringá',
    'uf': 'PR',
}


def criar_local(client):
    resposta = client.post('/locais', json=LOCAL)
    assert resposta.status_code == 201
    return resposta.json()


def test_crud_de_locais(client):
    local = criar_local(client)
    assert local['uf'] == 'PR'
    assert client.get(f"/locais/{local['id']}").json() == local
    assert client.get('/locais').json() == {'items': [local], 'total': 1}
    assert client.delete(f"/locais/{local['id']}").status_code == 204
    assert client.get(f"/locais/{local['id']}").status_code == 404


def test_local_invalido_e_inexistente(client):
    assert client.post('/locais', json={**LOCAL, 'nome': '  '}).status_code == 422
    assert client.get('/locais/invalido').status_code == 404
    assert client.get(f'/locais/{ObjectId()}/denuncias').status_code == 404


def test_denuncia_vinculada_ao_local(client):
    local = criar_local(client)
    criada = client.post('/denuncias', json={**DENUNCIA, 'local_id': local['id']}).json()
    assert criada['local_id'] == local['id']
    vinculadas = client.get(f"/locais/{local['id']}/denuncias").json()
    assert vinculadas['total'] == 1 and vinculadas['items'][0]['id'] == criada['id']
    assert client.get('/denuncias', params={'local_id': local['id']}).json()['total'] == 1
    assert client.get('/denuncias', params={'local_id': str(ObjectId())}).json()['total'] == 0


def test_denuncia_com_local_inexistente_e_rejeitada(client):
    resposta = client.post('/denuncias', json={**DENUNCIA, 'local_id': str(ObjectId())})
    assert resposta.status_code == 422
    assert client.get('/denuncias').json()['total'] == 0


def test_nao_exclui_local_com_denuncias(client):
    local = criar_local(client)
    client.post('/denuncias', json={**DENUNCIA, 'local_id': local['id']})
    assert client.delete(f"/locais/{local['id']}").status_code == 409
    assert client.get(f"/locais/{local['id']}").status_code == 200


def test_historico_de_status_como_subdocumentos(client):
    criada = client.post('/denuncias', json=DENUNCIA).json()
    assert [h['status_novo'] for h in criada['historico']] == ['registrada']
    client.patch(f"/denuncias/{criada['id']}", json={'titulo': 'Outro título aqui'})
    atual = client.patch(
        f"/denuncias/{criada['id']}",
        json={'status': 'em_analise', 'observacao': 'Equipe designada'},
    ).json()
    assert len(atual['historico']) == 2
    assert atual['historico'][1]['status_anterior'] == 'registrada'
    assert atual['historico'][1]['status_novo'] == 'em_analise'
    assert atual['historico'][1]['observacao'] == 'Equipe designada'
    padrao = client.patch(f"/denuncias/{criada['id']}", json={'status': 'resolvida'}).json()
    assert padrao['historico'][2]['observacao'] == 'Status atualizado.'


def test_atualizar_para_local_inexistente_e_rejeitado(client):
    criada = client.post('/denuncias', json=DENUNCIA).json()
    resposta = client.patch(f"/denuncias/{criada['id']}", json={'local_id': str(ObjectId())})
    assert resposta.status_code == 422
