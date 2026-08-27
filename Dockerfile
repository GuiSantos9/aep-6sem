# Imagem modelo 
FROM python:3.12.8-slim

# Mapeamento código-fonte
WORKDIR /app

# Dependências
COPY requirements.txt .

# Instalação de dependências quando criar a imagem
RUN pip install --no-cache-dir -r requirements.txt

# Diretório de trabalho (atual)
COPY . .

# Início execução
CMD ["python", "main.py"]