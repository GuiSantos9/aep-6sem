# ***Repositorio feito para a AEP do 6 semestre***

#### ***Alunos***
- Matheus Pintor Fernandes Ferreira.
- Guilherme Augusto dos Santos.


#### Temas da a serem debatidos
-> ODS 9: industra, inovação e infraestrutura

#### Possível stack (A ser discutido)
- linguagem: python.
- framework: fastapi, pytest(para testes unitarios).
- frontend: html, css, js.

#### Estrutura de pastas

projeto-denuncias/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Ponto de entrada FastAPI e inclusão de routers
│   ├── core/                    # Configurações globais e segurança
│   │   ├── __init__.py
│   │   ├── config.py            # Variáveis de ambiente (Pydantic BaseSettings)
│   │   ├── security.py          # Hashing de senhas, JWT e OAuth2
│   │   └── database.py          # Conexão e sessão do banco de dados (ex: SQLAlchemy)
│   │
│   ├── api/                     # Camada de endpoints/rotas
│   │   ├── __init__.py
│   │   ├── deps.py              # Injeção de dependências (get_db, get_current_user)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py           # Agrupador de rotas da v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py      # /login e autenticação
│   │           ├── denuncias.py # /denuncias (CRUD, filtros, ordenação por prioridade)
│   │           └── chamados.py  # /chamados (vincular órgão e justificativa)
│   │
│   ├── models/                  # Entidades do Banco de Dados (ORM)
│   │   ├── __init__.py
│   │   ├── user.py              # Tabela de Usuários
│   │   ├── denuncia.py          # Tabela de Denúncias
│   │   ├── chamado.py           # Tabela de Chamados
│   │   └── orgao.py             # Tabela de Órgãos/Instituições
│   │
│   ├── schemas/                 # Validação de dados de entrada/saída (Pydantic)
│   │   ├── __init__.py
│   │   ├── token.py             # Schemas de Token JWT
│   │   ├── user.py              # UserCreate, UserResponse
│   │   ├── denuncia.py          # DenunciaCreate, DenunciaResponse, DenunciaFilter
│   │   ├── chamado.py           # ChamadoCreate, ChamadoResponse
│   │   └── enums.py             # Enums (PrioridadeEnum: ALTA, MEDIA, BAIXA)
│   │
│   └── services/                # Regras de negócio e lógica de aplicação
│       ├── __init__.py
│       ├── auth_service.py      # Lógica de validação de credenciais
│       ├── denuncia_service.py  # Criação, busca e ordenação de ocorrências
│       └── chamado_service.py   # Regra de vínculo denúncia-órgão e justificativa
│
├── tests/                       # Estrutura de Testes com Pytest
│   ├── __init__.py
│   ├── conftest.py              # Fixtures globais (cliente de teste, banco em memória, auth token)
│   ├── test_auth.py             # Testes de login e geração de token
│   ├── test_denuncias.py        # Testes de cadastro, busca e ordenação por prioridade
│   └── test_chamados.py         # Testes de abertura e validação de chamados
│
├── alembic/                     # Migrações de banco de dados (se aplicável)
├── .env.example
├── .gitignore
├── requirements.txt (ou pyproject.toml)
└── README.md

# 🚀 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para configurar o ambiente e executar a API.

## 📋 Pré-requisitos
* Python **3.12.8** instalado ([python.org](https://www.python.org/downloads/release/python-3128/))

### 1. Clonar o Repositório
```bash
git clone https://github.com/GuiSantos9/aep-6sem.git
``` 

### 2. Criar e ativar o ambiente virtual
- se a pasta venv ainda não existir na maquina execut e o comando
```bash
python -m venv venv
```

- ative o ambiente virtual (windows)
```bash
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Verificar instalações
```bash
fastapi --version
uvicorn --version
pytest --version
python --version
```

### 5. Iniciar a API

```bash
fastapi dev main.py
```