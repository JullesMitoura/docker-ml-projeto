# Desenvolver o projeto de ML para predicao de eficiencia de troca termica


1. Criar o ambiente virtual (.venv)
```python
python -m venv .venv
```

2. Ativar o ambiente virtual
- macos:
```python
source .venv/bin/activate
```

- win:
```python
.venv\Scripts\activate.bat
```

3. Instalar as dependencias:
```python
pip install -r requirements.txt
```

4. Criar a imagem:
```python
docker build -t docker-ml-projeto .
```

5. Executar o container:
```python
docker run docker-ml-projeto
```

---
### Comandos de Docker

Comandos básicos de Docker:

- `docker ps` — verifica quais containers estão rodando na máquina.
- `docker run hello-world` — executa uma imagem de teste do Docker Hub.

Após isso, podemos executar novamente o `docker ps` e ver os detalhes das imagens. Nesse caso, não teremos resultados pois o container anterior foi executado e finalizado. Para verificar os que já foram finalizados:

- `docker ps -a` — lista todos os containers já executados.

Por hora, esses comandos ainda não são úteis, mas isso é parte do ciclo de introdução. Mais detalhes serão abordados em outros módulos.

Podemos também rodar o Ubuntu dentro de um container:

```bash
docker run -it ubuntu bash
```

O parâmetro `-it` permite interagir com o container e o `bash` abre o terminal dentro do Ubuntu. Com o container rodando, podemos verificá-lo com `docker ps`.

Para parar um container:

```bash
docker stop "CONTAINER ID"
```

Para iniciar novamente um container parado:

```bash
docker start "CONTAINER ID"
```

Para voltar a executar comandos dentro do container:

```bash
docker exec -it "CONTAINER ID" bash
```