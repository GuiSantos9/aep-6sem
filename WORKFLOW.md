# Fluxo do Sistema

## Ciclo de vida de uma denúncia

```text
[ POST /denuncias ]
   └── Cria a denúncia com status "registrada"
           │
           ▼
[ GET /denuncias ]
   └── Lista denúncias com filtros opcionais (tipo, prioridade)
           │
           ▼
[ PATCH /denuncias/{id} ]
   └── Atualiza campos: descrição, tipo, prioridade, status etc.
           │
           ▼
[ DELETE /denuncias/{id} ]
   └── Remove a denúncia
```

## Status possíveis

| Status | Descrição |
|---|---|
| `registrada` | Denúncia recém-criada |
| `em_analise` | Em avaliação |
| `encaminhada` | Encaminhada para tratamento |
| `resolvida` | Ocorrência resolvida |
| `arquivada` | Arquivada sem resolução |

## Tipos de arquitetura hostil

| Valor | Descrição |
|---|---|
| `banco_dividido` | Banco com divisória que impede deitar |
| `espigao_metalico` | Espigões em superfícies |
| `inclinacao_de_superficie` | Superfície inclinada para impedir permanência |
| `retirada_de_assento` | Remoção de assentos públicos |
| `barreira_fisica` | Obstáculo físico de acesso |
| `emissao_sonora` | Som irritante para afastar pessoas |
| `aspersor_de_agua` | Aspersores para impedir permanência |
| `outro` | Outras formas |
