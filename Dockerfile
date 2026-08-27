# Imagem modelo 
FROM python:3.12.8-slim

# Mapeamento código-fonte
WORKDIR /app

# Dependências
COPY requirements.txt .

# Instalação de dependências quando criar a imagem
RUN python - m pip install --no-cache-dir.

# Diretório de trabalho (atual)
COPY pyproject.toml README.md ./
COPY app ./app
COPY db ./db

EXPOSE 8000

# Início execução
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]