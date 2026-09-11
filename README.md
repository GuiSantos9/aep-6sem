# Inóspita API

Sistema para registrar, consultar e acompanhar denúncias de arquitetura hostil em espaços urbanos, como bancos com divisórias, espigões metálicos e barreiras físicas. As ocorrências podem ser classificadas por tipo, prioridade e status.

O projeto tem três componentes:

| Componente | Tecnologia | Endereço durante o desenvolvimento |
| --- | --- | --- |
| Frontend | HTML, CSS e JavaScript | [http://localhost:5500](http://localhost:5500) |
| API | Python e FastAPI | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Banco de dados | MongoDB | Configurado por `MONGO_URI` |

**Sequência de inicialização: MongoDB → API → frontend.** Com Docker Compose, o banco e a API são iniciados juntos. O frontend deve ser servido separadamente em ambas as opções abaixo.

## 0. Resultado dos testes
88 testes aprovados em Python 3.12.14 (Linux). Cobertura de linhas e ramificações combinadas: 99,44%, acima do mínimo de 70%. São 321 de 323 instruções executáveis cobertas (99,38%) e 36 de 36 ramificações cobertas (100%). Os testes originais foram preservados.

A medição abrange todo o backend Python em app/ e db/, sem exclusões de módulos da aplicação. Não mede o JavaScript, HTML ou CSS em front/. Se a rubrica exigir cobertura do frontend, ela deverá ser medida separadamente com ferramentas JavaScript.

## 1. Preparação

Clone o repositório ou baixe e extraia seu ZIP. Abra um terminal na **raiz do projeto**, a pasta que contém `requirements.txt`, `docker-compose.yaml`, `app/` e `front/`.

Escolha uma das opções para o backend:

- **Opção A — Docker:** Docker com Compose instalado e em execução. No Windows, abra o Docker Desktop. Para servir o frontend com os comandos deste guia, instale também Python 3.12; alternativamente, use o Live Server do VS Code.
- **Opção B — execução local:** Python 3.12 e uma instância MongoDB acessível, instalada localmente ou hospedada. O serviço MongoDB deve estar em execução antes de iniciar a API.

Os comandos Windows abaixo funcionam no CMD e no PowerShell, sem precisar ativar o ambiente virtual. No Linux/macOS, use `python3` se o comando `python` não existir.

## 2. Iniciar o backend

### Opção A — MongoDB e API com Docker Compose

**Crie `.env` somente se ele ainda não existir**, para preservar configurações locais.

Windows:

```powershell
copy .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

Edite `.env` e defina `MONGO_USER`, `MONGO_PASSWORD` e `DB_NAME`. O arquivo de exemplo contém valores para desenvolvimento; não publique credenciais reais no repositório.

Inicie os serviços:

```bash
docker compose up --build
```

Aguarde a inicialização do MongoDB e a mensagem de conclusão da inicialização da API. Mantenha esse terminal aberto. **Não execute Uvicorn separadamente nesta opção**, pois a API já está no contêiner.

O Compose monta a URI do banco usando `MONGO_USER`, `MONGO_PASSWORD` e `DB_NAME`, com o endereço interno `mongodb:27017`. A API fica acessível na porta 8000 do computador. O MongoDB do Compose não tem porta publicada no computador; portanto, essa configuração não atende uma API executada localmente fora dos contêineres.

Continue na seção **3. Conferir a API** e depois inicie o frontend.

### Opção B — API local com ambiente virtual

Primeiro, disponibilize seu MongoDB. Crie `.env` a partir de `.env.example`, usando o comando de cópia da opção A, caso o arquivo ainda não exista.

Configure `MONGO_URI` e `DB_NAME` para sua instância. Exemplo para um MongoDB local **sem autenticação**, em ambiente de desenvolvimento:

```dotenv
MONGO_URI=mongodb://localhost:27017
DB_NAME=inospita
```

Se o MongoDB exigir autenticação, use a URI correspondente às suas credenciais e ao banco de autenticação. Para uma instância hospedada, use a URI fornecida pelo serviço e autorize o acesso do seu computador.

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m uvicorn app.main:app --reload
```

No Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --reload
```

Mantenha o terminal aberto. A opção `--reload` reinicia a API quando o código muda e é destinada ao desenvolvimento.

## 3. Conferir a API

Após a inicialização, abra:

- [Status da API](http://localhost:8000/health): deve retornar JSON com `"status": "ok"`.
- [Documentação interativa](http://localhost:8000/docs): permite consultar e testar as rotas.

Na inicialização, a aplicação cria os índices do banco e insere denúncias de exemplo **somente se a coleção estiver vazia**.

## 4. Iniciar e abrir o frontend

Em **outro terminal**, também na raiz do projeto, inicie um servidor para a pasta `front`.

Se você usou Docker e tem Python instalado no computador:

```bash
python -m http.server 5500 --bind 127.0.0.1 --directory front
```

No Linux/macOS, use `python3` se necessário.

Se criou o ambiente virtual local, no Windows:

```powershell
.venv\Scripts\python -m http.server 5500 --bind 127.0.0.1 --directory front
```

No Linux/macOS:

```bash
.venv/bin/python -m http.server 5500 --bind 127.0.0.1 --directory front
```

Abra **[http://localhost:5500](http://localhost:5500)**. O servidor entrega `front/index.html` automaticamente. Mantenha esse segundo terminal aberto.

Como alternativa, abra `front/index.html` com a extensão **Live Server** do VS Code e use o endereço informado pela extensão.

O frontend chama a API pelo endereço definido em `front/app.js`:

```javascript
const BASE_URL = 'http://localhost:8000';
```

Se alterar a porta ou o endereço da API, atualize esse valor. O servidor do frontend apenas entrega HTML, CSS e JavaScript; a API e o banco precisam continuar em execução para consultar ou salvar denúncias.

## 5. Executar os testes e medir cobertura

Os testes usam `pytest`, `pytest-cov` e MongoDB simulado com `mongomock`. **Não exigem Docker, MongoDB real, Uvicorn ou frontend em execução.** O banco simulado existe apenas nos testes.

Na raiz do projeto, crie o ambiente virtual se ainda não existir e instale as dependências. No Windows:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pip install "pytest-cov>=6,<8"
.venv\Scripts\python -m pytest
```

Se `.venv` já existir, pule o primeiro comando. No Linux/macOS, use `python3 -m venv .venv` e substitua `.venv\Scripts\python` por `.venv/bin/python` nos comandos seguintes.

Na versão com a suíte ampliada, `pytest.ini` configura a medição de todo o backend (`app/` e `db/`), incluindo ramificações, e exige no mínimo **70%**. Um teste reprovado ou cobertura abaixo do limite faz o comando terminar com erro.

Para solicitar explicitamente a medição:

```powershell
.venv\Scripts\python -m pytest --cov=app --cov=db --cov-branch --cov-report=term-missing --cov-report=html --cov-report=xml --cov-fail-under=70
```

Relatórios gerados:

| Saída | Como consultar |
| --- | --- |
| Terminal | Resultado dos testes, percentual e linhas não cobertas. |
| `coverage.xml` | Relatório para ferramentas de análise e integração contínua. |

A suíte ampliada foi validada com **88 testes aprovados e 99,44% de cobertura combinada de linhas e ramificações**. Esse resultado corresponde à versão testada; execute novamente após alterações. A cobertura é do backend Python, não do frontend. O banco simulado não comprova conectividade ou autenticação com um MongoDB real.

## 6. Encerrar os serviços

- Frontend e API local: pressione `Ctrl+C` no terminal de cada servidor.
- Docker Compose: pressione `Ctrl+C` no terminal e execute `docker compose down` para remover os contêineres e a rede do projeto.

O volume `mongo_data` mantém os dados do banco entre execuções. `docker compose down` sem `-v` preserva esse volume.

## Variáveis de ambiente

| Variável | Uso |
| --- | --- |
| `MONGO_USER` | Usuário inicial do MongoDB no Compose. |
| `MONGO_PASSWORD` | Senha inicial do MongoDB no Compose. |
| `DB_NAME` | Banco utilizado pela aplicação, nas duas opções de execução. |
| `MONGO_URI` | URI usada pela API local. No Compose, ela é montada e injetada no contêiner. |
| `APP_NAME` | Opcional: nome retornado por `/health`; padrão `Inóspita API`. |

## Solução de problemas

| Problema | O que verificar |
| --- | --- |
| `unrecognized arguments: --cov...` | Instale o plugin no mesmo ambiente: `.venv\Scripts\python -m pip install "pytest-cov>=6,<8"`. |
| `No module named uvicorn` ou outra dependência ausente | Execute `.venv\Scripts\python -m pip install -r requirements.txt`. |
| Variável `MONGO_URI` ou `DB_NAME` ausente | Confira o `.env` na raiz e os nomes das variáveis. No Windows, verifique se o arquivo não foi salvo como `.env.txt`. |
| Erro de conexão com MongoDB | Confira se o banco está disponível e se URI, credenciais e permissões de acesso estão corretas. |
| Erro de autenticação após mudar credenciais do Compose | As credenciais iniciais são aplicadas na criação do banco; alterar `.env` não altera usuários de um volume já existente. Use as credenciais válidas ou atualize o usuário no MongoDB. |
| Porta 8000 ou 5500 ocupada | Encerre o processo que ocupa a porta ou configure outra. Se mudar a porta da API, atualize `BASE_URL` no frontend. |
| Interface abre, mas não carrega ou salva dados | Acesse `/health`, confira `BASE_URL` e verifique se API e banco continuam em execução. |
| Página 404 na porta 5500 | Execute o servidor na raiz com `--directory front` e confirme que `front/index.html` existe. |
| Docker não conecta ao serviço | Abra o Docker Desktop ou inicie o serviço Docker antes de executar Compose. |

## Estrutura do projeto

| Caminho | Responsabilidade |
| --- | --- |
| `app/main.py` | Aplicação FastAPI, CORS, tratamento de erros e health check. |
| `app/routers/` | Rotas HTTP das denúncias. |
| `app/schemas/` | Validação e formatos de entrada e saída. |
| `app/services/` | Regras e operações de negócio. |
| `app/repositories/` | Consultas e gravações no MongoDB. |
| `app/entities/`, `app/enums/`, `app/exceptions.py` | Tipos, classificações e exceções de domínio. |
| `db/connection.py` | Configuração, índices e ciclo da conexão. |
| `db/seed.py` | Dados iniciais de exemplo. |
| `front/` | Interface HTML, CSS e JavaScript. |
| `tests/` | Testes automatizados e fixtures. |
| `pytest.ini`, `.coveragerc` | Configuração da suíte ampliada e cobertura. |
| `requirements.txt` | Dependências Python. |
| `.env.example` | Modelo de configuração local. |
| `Dockerfile`, `docker-compose.yaml` | Imagem da API e serviços de execução. |
