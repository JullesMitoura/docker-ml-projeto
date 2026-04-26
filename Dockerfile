# passo 01: escolher a imagem base
FROM python:3.11-slim

# -slim: traz uma versão mais leve do python

# passo 02: definir o ditetorio de trabalho do container
WORKDIR /app

# app
# - projeto

# passo 03: instalacao de dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --no-cache-dir: evita que o pip armazene os arquivos de instalação em cache, 
# reduzindo o tamanho da imagem final

# passo 04: copiar o codigo para o container
COPY src/ src/
COPY data/ data/

# a estrutura do projeto dentro do container sera:
# /app
#  - src (aqui vem todo o projeto conforme definido no src/)
#  - data

# passo 05: definir variaveis de ambiente
ENV DB_PATH="data/heat_exchanger.db"\
    MODEL_PATH="artifacts/heat_efficiency_model.pkl"

# para realizar inferencias, podemos bypassar o comando de exeucao indicado
# docker run docker-ml-projeto sh -c "python src/train.py && python src/inference.py --efficiency 300"

# passo 06: definir o comando de execucao do container
CMD ["python", "src/train.py"]