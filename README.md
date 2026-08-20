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
