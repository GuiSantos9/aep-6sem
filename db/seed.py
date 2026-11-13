from datetime import datetime, timezone

from pymongo.database import Database

LOCAIS_SEED = [
    {"nome": "Largo do Rosário", "bairro": "Centro", "cidade": "Maringá", "uf": "PR", "referencia": "Próximo à Catedral"},
    {"nome": "Avenida Brasil, 1200", "bairro": "Zona 01", "cidade": "Maringá", "uf": "PR", "referencia": "Prédio comercial com marquise"},
    {"nome": "Praça da Juventude", "bairro": "Zona 07", "cidade": "Maringá", "uf": "PR", "referencia": None},
]

SEED = [
    {
        "titulo": "Banco com divisória no Largo do Rosário",
        "descricao": (
            "Banco público instalado com barras metálicas centrais que impedem "
            "pessoas em situação de rua de se deitarem. Estrutura em péssimo estado "
            "de conservação e sem qualquer sinalização."
        ),
        "tipo": "banco_dividido",
        "prioridade": "alta",
        "status": "registrada",
        "logradouro": "Largo do Rosário",
        "numero": "s/n",
        "complemento": None,
        "bairro": "Centro",
        "cidade": "Maringá",
        "uf": "PR",
        "cep": "87013-010",
        "evidencias": [],
        "criado_em": datetime(2026, 8, 10, 14, 30, tzinfo=timezone.utc),
    },
    {
        "titulo": "Espigões metálicos sob marquise na Av. Brasil",
        "descricao": (
            "Espigões de metal foram instalados sob a marquise de prédio comercial, "
            "impedindo que pessoas usem o espaço coberto como abrigo durante chuvas. "
            "Risco de ferimentos graves."
        ),
        "tipo": "espigao_metalico",
        "prioridade": "urgente",
        "status": "em_analise",
        "logradouro": "Avenida Brasil",
        "numero": "1200",
        "complemento": None,
        "bairro": "Zona 01",
        "cidade": "Maringá",
        "uf": "PR",
        "cep": "87013-000",
        "evidencias": [],
        "criado_em": datetime(2026, 8, 15, 9, 0, tzinfo=timezone.utc),
    },
    {
        "titulo": "Superfície inclinada na Praça da Juventude",
        "descricao": (
            "Área de descanso da praça apresenta inclinação artificial que torna "
            "impossível sentar ou deitar no local. A modificação foi feita "
            "intencionalmente para afastar pessoas em situação de vulnerabilidade."
        ),
        "tipo": "inclinacao_de_superficie",
        "prioridade": "media",
        "status": "registrada",
        "logradouro": "Praça da Juventude",
        "numero": "s/n",
        "complemento": None,
        "bairro": "Zona 07",
        "cidade": "Maringá",
        "uf": "PR",
        "cep": "87020-000",
        "evidencias": [],
        "criado_em": datetime(2026, 9, 1, 17, 45, tzinfo=timezone.utc),
    },
]


def seed_locais(database: Database) -> None:
    if database.locais.count_documents({}) == 0:
        agora = datetime.now(timezone.utc)
        database.locais.insert_many([{**l, "criado_em": agora} for l in LOCAIS_SEED])
        print(f"Seed: {len(LOCAIS_SEED)} locais inseridos.")


def seed_denuncias(database: Database) -> None:
    if database.denuncias.count_documents({}) == 0:
        locais = [database.locais.find_one({"nome": l["nome"]}) for l in LOCAIS_SEED]
        documentos = []
        for denuncia, local in zip(SEED, locais):
            documento = {
                **denuncia,
                "local_id": str(local["_id"]) if local else None,
                "historico": [
                    {
                        "status_anterior": None,
                        "status_novo": "registrada",
                        "observacao": "Denúncia registrada.",
                        "data": denuncia["criado_em"],
                    }
                ],
            }
            documentos.append(documento)
        database.denuncias.insert_many(documentos)
        print(f"Seed: {len(SEED)} denúncias inseridas.")
