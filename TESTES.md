# Testes automatizados — Inóspita API

## Resultado verificado

88 testes aprovados em Python 3.12.14 (Linux). Cobertura de linhas e ramificações combinadas: **99,44%**, acima do mínimo de 70%. São 321 de 323 instruções executáveis cobertas (99,38%) e 36 de 36 ramificações cobertas (100%). Os testes originais foram preservados.

A medição abrange todo o backend Python em `app/` e `db/`, sem exclusões de módulos da aplicação. Não mede o JavaScript, HTML ou CSS em `front/`. Se a rubrica exigir cobertura do frontend, ela deverá ser medida separadamente com ferramentas JavaScript.

## Executar no Windows

Na pasta que contém `pytest.ini`, com Python 3.12 instalado:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest
```

Não é necessário ativar o ambiente, iniciar Uvicorn, criar `.env` ou subir MongoDB. Os testes usam banco temporário em memória por caso, sem acessar dados reais.

No Linux/macOS, substitua `.venv\Scripts\python` por `.venv/bin/python`.

Se o ambiente já estiver ativo:

```bash
python -m pytest
```

O `pytest.ini` já configura cobertura, relatórios e limite de 70%. O processo retorna erro caso haja teste reprovado ou cobertura inferior ao mínimo.

Comando explícito equivalente de cobertura:

```bash
python -m pytest --cov=app --cov=db --cov-branch --cov-report=term-missing --cov-report=html --cov-report=xml --cov-fail-under=70
```

## Evidências para entregar

- `htmlcov/index.html`: abra no navegador; mantenha a pasta inteira para funcionar.
- `coverage.xml`: resultado de cobertura em formato processável.
- `reports/pytest.txt`: saída da execução verificada.
- `reports/junit.xml`: resultado dos 88 casos.
- `reports/ambiente-validado.txt`: versões exatas instaladas no ambiente Linux da validação, para referência; inclui dependências específicas de Linux, portanto não é um arquivo de instalação para Windows.

Para atualizar o JUnit: `python -m pytest --junitxml=reports/junit.xml`.

## Organização e comportamentos verificados

| Arquivo | Objetivo |
| --- | --- |
| `tests/test_denuncias.py` | Dois testes originais: CRUD e ID inválido. |
| `tests/test_api.py` | Integração HTTP: criação, consulta, exclusão, defaults, normalização, atualização parcial, status, campos obrigatórios, limites de tamanho, URLs, CEP, enums, dados nulos, filtros combinados, ordenação e paginação. Validações rejeitadas devem preservar os dados. |
| `tests/test_database.py` | Precedência de configuração, variável ausente, índices, seed inicial e repetido, preservação de dados existentes, inicialização e fechamento da conexão mesmo quando o corpo do lifespan falha. |
| `tests/test_service_repository.py` | IDs inválidos/ausentes, ausência de inserção acidental e desaparecimento de registro entre consulta e escrita. |
| `tests/conftest.py` | Banco isolado por teste HTTP e limpeza com `finally`. |

Casos parametrizados contam individualmente: uma mesma função é executada com diferentes entradas. Asserções verificam respostas, conteúdo e persistência, não apenas execução de linhas.

## Limites e alterações

- Rotas, validação, serviços e repositório são reais nos testes HTTP; o banco é `mongomock`. Esses testes não comprovam autenticação, rede, disponibilidade ou comportamento de um servidor MongoDB real.
- O ciclo de conexão usa um cliente substituto controlado. Não foi executado teste de infraestrutura com Docker/MongoDB real nem teste visual do frontend.
- As duas instruções não cobertas são os handlers de `ConflictError` e `BusinessRuleError` em `app/main.py`, pois os fluxos de negócio atuais não lançam essas exceções. Não foram criadas regras fictícias para aumentar o percentual.
- Há dois avisos de descontinuação em dependências Starlette/AnyIO na execução registrada; nenhum teste falhou. As faixas de versões em `requirements.txt` permitem atualizações futuras.
- O código funcional em `app/`, `db/` e `front/` foi mantido. Foram adicionados testes, configuração, dependência de cobertura e documentação. A fixture existente ganhou limpeza garantida.
- O ZIP de entrega não inclui ambiente virtual, caches, histórico Git ou `.env` com credenciais. Mantenha o seu `.env` local para executar a aplicação.

Cobertura alta demonstra execução do código nesses cenários; não é garantia de ausência de defeitos nem substitui requisitos de negócio adicionais.
