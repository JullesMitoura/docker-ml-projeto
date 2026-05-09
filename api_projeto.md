# API REST — plano de aplicação

FastAPI sobre o modelo treinado. Carrega o pickle uma vez e expõe
predições em HTTP.

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/predict/efficiency` | `{dia}` → eficiência |
| `POST` | `/predict/day` | `{eficiencia}` → dia |

**Arquivos**

```
src/api.py                       NOVO
src/inference.py                 ALTERADO (predict_* retorna float)
requirements-inference.txt       ALTERADO (+fastapi, +uvicorn)
Dockerfile.inference             ALTERADO (uvicorn + EXPOSE 8080)
```

---

## 1. `requirements-inference.txt`

```txt
pandas==3.0.2
scikit-learn==1.8.0
python-dotenv==1.2.2
fastapi==0.115.0
uvicorn[standard]==0.32.0
```

---

## 2. `src/inference.py`

Adicione `return` em `predict_eff`/`predict_data` e um `get_model()`
cacheado. CLI continua funcionando.

```python
import argparse
import os
import pickle
from functools import lru_cache

import numpy as np
from dotenv import load_dotenv

from utils.logger import get_logger
from utils.versioning import list_versions, resolve_version

load_dotenv(override=True)
MODEL_PATH = os.getenv("MODEL_PATH")
logger = get_logger(__name__)


def load_model(model_path: str):
    with open(model_path, "rb") as f:
        bundle = pickle.load(f)
    logger.info("R² Score: %.4f | %s", bundle["metrics"], bundle["description"])
    return bundle["model"]


@lru_cache(maxsize=1)
def get_model():
    return load_model(resolve_version(None))


def predict_eff(model, dia: int) -> float:
    res = float(model.predict(np.array([dia]).reshape(1, -1))[0])
    logger.info("Dia %s | eficiência: %.4f", dia, res)
    return res


def predict_data(model, eficiencia: float) -> float:
    dia = float((eficiencia - model.intercept_) / model.coef_[0])
    logger.info("Eficiência %s | dia: %.4f", eficiencia, dia)
    return dia


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--efficiency", type=int)
    group.add_argument("--data", type=float)
    parser.add_argument("--version", type=str, default=None)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        for name in list_versions():
            print(name)
    else:
        model = load_model(resolve_version(args.version))
        if args.efficiency is not None:
            predict_eff(model, args.efficiency)
        elif args.data is not None:
            predict_data(model, args.data)
```

---

## 3. `src/api.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel

from inference import get_model, predict_data, predict_eff

app = FastAPI(title="Heat Efficiency API")


class EfficiencyRequest(BaseModel):
    dia: int


class DayRequest(BaseModel):
    eficiencia: float


@app.post("/predict/efficiency")
def predict_efficiency(req: EfficiencyRequest):
    return {"predicao": predict_eff(get_model(), req.dia)}


@app.post("/predict/day")
def predict_day(req: DayRequest):
    return {"predicao": predict_data(get_model(), req.eficiencia)}
```

---

## 4. `Dockerfile.inference`

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements-inference.txt .
RUN pip install --no-cache-dir -r requirements-inference.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY src/ src/

ENV MODEL_PATH="artifacts/heat_efficiency_model.pkl" \
    PYTHONPATH=/app/src

EXPOSE 8080
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 5. Como rodar

```bash
pip install -r requirements-inference.txt
cd src && uvicorn api:app --reload --port 8080
open http://localhost:8080/docs
```

```bash
curl -X POST http://localhost:8080/predict/efficiency \
  -H 'Content-Type: application/json' -d '{"dia": 30}'

curl -X POST http://localhost:8080/predict/day \
  -H 'Content-Type: application/json' -d '{"eficiencia": 92.5}'
```

**Docker:**
```bash
docker build -f Dockerfile.inference -t docker-ml-projeto-inference .
docker run --rm -p 8080:8080 \
  -v $(pwd)/artifacts:/app/artifacts \
  docker-ml-projeto-inference
```
