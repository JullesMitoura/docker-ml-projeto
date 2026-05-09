from fastapi import FastAPI
from pydantic import BaseModel

from src.inference import get_model, predict_data, predict_eff

app = FastAPI(title="Heat Efficiency API")


class EfficiencyRequest(BaseModel):
    dia: int


class DayRequest(BaseModel):
    eficiencia: float

class OutputEffResponse(BaseModel):
    predicao: float

class OutputDayResponse(BaseModel):
    day: float


@app.post("/predict/efficiency")
def predict_efficiency(req: EfficiencyRequest) -> OutputEffResponse:
    res = predict_eff(get_model(), req.dia)
    return OutputEffResponse(predicao=res)


@app.post("/predict/day")
def predict_day(req: DayRequest) -> OutputDayResponse:
    day = predict_data(get_model(), req.eficiencia)
    return OutputDayResponse(day=day)