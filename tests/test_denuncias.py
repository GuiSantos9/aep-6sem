DENUNCIA_VALIDA = {
    "titulo": "Banco público com divisórias",
    "descricao": "Banco instalado com barras que impedem uma pessoa de se deitar.",
    "tipo": "banco_dividido",
    "prioridade": "alta",
    "logradouro": "Praça da Inclusão",
    "numero": "100",
    "bairro": "Centro",
    "cidade": "Maringá",
    "uf": "pr",
    "cep": "87000-000",
    "latitude": -23.4205,
    "longitude": -51.9333,
    "evidencias": ["https://example.com/evidencia-1.jpg"],
}


def criar_denuncia(client) -> dict:
    response = client.post("/denuncias", json=DENUNCIA_VALIDA)
    assert response.status_code == 201
    return response.json()


def test_crud_de_denuncia(client):
    criada = criar_denuncia(client)
    denuncia_id = criada["id"]
    assert len(denuncia_id) == 24
    assert criada["status"] == "registrada"
    assert criada["uf"] == "PR"

    response = client.get("/denuncias?prioridade=alta&cidade=Maringá")
    assert response.status_code == 200
    assert response.json()["total"] == 1

    response = client.patch(
        f"/denuncias/{denuncia_id}",
        json={"prioridade": "urgente", "status": "em_analise"},
    )
    assert response.status_code == 200
    assert response.json()["prioridade"] == "urgente"
    assert response.json()["status"] == "em_analise"

    response = client.delete(f"/denuncias/{denuncia_id}")
    assert response.status_code == 204
    assert client.get(f"/denuncias/{denuncia_id}").status_code == 404


def test_vinculo_encaminha_denuncia_e_impede_duplicidade(client):
    denuncia_id = criar_denuncia(client)["id"]
    vinculo = {
        "orgao_nome": "Secretaria Municipal de Urbanismo",
        "orgao_tipo": "Órgão municipal",
        "contato": "urbanismo@example.gov.br",
        "protocolo": "URB-2026-001",
    }

    response = client.post(f"/denuncias/{denuncia_id}/vinculos", json=vinculo)
    assert response.status_code == 201
    vinculo_id = response.json()["id"]
    assert response.json()["orgao_nome"] == vinculo["orgao_nome"]

    denuncia = client.get(f"/denuncias/{denuncia_id}").json()
    assert denuncia["status"] == "encaminhada"
    assert len(denuncia["vinculos"]) == 1

    response = client.post(f"/denuncias/{denuncia_id}/vinculos", json=vinculo)
    assert response.status_code == 409

    response = client.delete(
        f"/denuncias/{denuncia_id}/vinculos/{vinculo_id}"
    )
    assert response.status_code == 204
    denuncia = client.get(f"/denuncias/{denuncia_id}").json()
    assert denuncia["status"] == "em_analise"


def test_nao_encaminha_sem_vinculo(client):
    denuncia_id = criar_denuncia(client)["id"]

    response = client.patch(
        f"/denuncias/{denuncia_id}",
        json={"status": "encaminhada"},
    )
    assert response.status_code == 422
    assert "vínculo" in response.json()["detail"]


def test_exige_latitude_e_longitude_juntas(client):
    payload = DENUNCIA_VALIDA | {"longitude": None}
    response = client.post("/denuncias", json=payload)

    assert response.status_code == 422
    assert "juntas" in response.json()["detail"]


def test_object_id_invalido_retorna_404(client):
    response = client.get("/denuncias/id-invalido")
    assert response.status_code == 404
