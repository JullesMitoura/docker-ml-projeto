from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.inference import get_model, predict_data, predict_eff
from src.utils.versioning import list_versions

app = FastAPI(title="Heat Efficiency API")


class EfficiencyRequest(BaseModel):
    dia: int = Field(..., ge = 0)

class DayRequest(BaseModel):
    eficiencia: float = Field(..., ge = 0, le = 100)

class OutputEffResponse(BaseModel):
    predicao: float

class OutputDayResponse(BaseModel):
    day: float


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def list_models():
    models = list_versions()
    return models

@app.post("/predict/efficiency")
def predict_efficiency(req: EfficiencyRequest) -> OutputEffResponse:
    try:
        res = predict_eff(get_model(), req.dia)
    except Exception as e:
        return {"error": str(e)}
    return OutputEffResponse(predicao=res)


@app.post("/predict/day")
def predict_day(req: DayRequest) -> OutputDayResponse:
    try:
        day = predict_data(get_model(), req.eficiencia)
    except Exception as e:
        return {"error": str(e)}
    return OutputDayResponse(day=day)