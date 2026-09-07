from datetime import datetime, timezone

from pymongo.database import Database

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


def seed_denuncias(database: Database) -> None:
    if database.denuncias.count_documents({}) == 0:
        database.denuncias.insert_many(SEED)
        print(f"Seed: {len(SEED)} denúncias inseridas.")
