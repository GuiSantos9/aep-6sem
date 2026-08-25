🏙️ Inóspita

Plataforma de gerenciamento de denúncias de arquitetura hostil

O Inóspita é uma plataforma desenvolvida como projeto da AEP do 6º semestre, com o objetivo de possibilitar o registro, gerenciamento e acompanhamento de denúncias relacionadas à arquitetura hostil nos espaços urbanos.

A proposta busca utilizar a tecnologia como ferramenta de apoio à identificação de situações que dificultam ou impedem a permanência e a circulação de pessoas em determinados espaços públicos.

🎯 Objetivo

Desenvolver uma plataforma capaz de:

📍 Registrar denúncias relacionadas à arquitetura hostil;
📝 Armazenar informações e evidências das ocorrências;
🔎 Permitir a consulta e filtragem de denúncias;
🚨 Classificar ocorrências de acordo com sua prioridade;
🏛️ Vincular denúncias a órgãos ou instituições responsáveis;
📊 Facilitar o acompanhamento e gerenciamento dos chamados;
🌎 Contribuir para a discussão sobre espaços urbanos mais acessíveis e inclusivos.
🌱 ODS relacionado

O projeto está relacionado ao:

ODS 9 — Indústria, Inovação e Infraestrutura

Construir infraestruturas resilientes, promover a industrialização inclusiva e sustentável e fomentar a inovação.

A utilização de tecnologia para registrar e organizar informações sobre problemas presentes no espaço urbano está alinhada à proposta de utilizar inovação e infraestrutura tecnológica como ferramentas para a melhoria da sociedade.

🛠️ Tecnologias
Backend
<p align="left"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="45" alt="Python"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="45" alt="FastAPI"/> </p>
Python — linguagem principal;
FastAPI — desenvolvimento da API REST;
Pytest — testes automatizados e testes unitários.
Banco de dados
<p align="left"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg" width="45" alt="MongoDB"/> </p>
MongoDB — armazenamento dos dados da aplicação.
Infraestrutura
<p align="left"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="45" alt="Docker"/> </p>
Docker — containerização da aplicação (em implementação).
Frontend
HTML
CSS
JavaScript

🚧 O frontend e a infraestrutura com Docker estão em desenvolvimento.

👨‍💻 Desenvolvedores
Matheus Pintor Fernandes Ferreira
Guilherme Augusto dos Santos
📂 Estrutura do Projeto
projeto-denuncias/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Ponto de entrada da aplicação FastAPI
│   │
│   ├── core/                    # Configurações globais e segurança
│   │   ├── __init__.py
│   │   ├── config.py            # Variáveis de ambiente
│   │   ├── security.py          # Hashing, JWT e OAuth2
│   │   └── database.py          # Conexão com o MongoDB
│   │
│   ├── api/                     # Camada de endpoints/rotas
│   │   ├── __init__.py
│   │   ├── deps.py              # Injeção de dependências
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py           # Agrupador de rotas da API v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py      # Autenticação
│   │           ├── denuncias.py # CRUD e filtros de denúncias
│   │           └── chamados.py  # Gerenciamento de chamados
│   │
│   ├── models/                  # Modelos das entidades
│   │   ├── __init__.py
│   │   ├── user.py              # Usuários
│   │   ├── denuncia.py          # Denúncias
│   │   ├── chamado.py           # Chamados
│   │   └── orgao.py             # Órgãos e instituições
│   │
│   ├── schemas/                 # Validação de dados com Pydantic
│   │   ├── __init__.py
│   │   ├── token.py             # Schemas de autenticação
│   │   ├── user.py              # Dados de usuários
│   │   ├── denuncia.py          # Dados de denúncias
│   │   ├── chamado.py           # Dados de chamados
│   │   └── enums.py              # Enumerações de prioridade
│   │
│   └── services/                # Regras de negócio
│       ├── __init__.py
│       ├── auth_service.py      # Autenticação
│       ├── denuncia_service.py  # Gerenciamento de denúncias
│       └── chamado_service.py   # Gerenciamento de chamados
│
├── tests/                       # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py              # Fixtures globais
│   ├── test_auth.py             # Testes de autenticação
│   ├── test_denuncias.py        # Testes de denúncias
│   └── test_chamados.py         # Testes de chamados
│
├── .env.example                 # Exemplo de variáveis de ambiente
├── .gitignore
├── requirements.txt             # Dependências do projeto
└── README.md

🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar o ambiente de desenvolvimento e executar a API.

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
