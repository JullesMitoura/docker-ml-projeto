# aqui desenvovlemos o processo de treino do modelo
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sqlalchemy import create_engine
from utils.logger import get_logger

logger = get_logger(__name__)

# funcao para leitura do dataset
def read_dataset(path):
    logger.info("Carregando o dataset...")
    engine = create_engine(f'sqlite:///{path}')
    df = pd.read_sql_query(
        "SELECT timestamp, heat_efficiency FROM heat_exchanger ORDER BY timestamp",
        engine,
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day_index"] = (df["timestamp"] - df["timestamp"].min()).dt.days
    return df

# funcao para treinar o modelo
def train(x:np.ndarray, y:np.ndarray) -> LinearRegression:
    logger.info("Treinando o modelo...")
    model = LinearRegression()
    model.fit(x, y)
    return model

# funcao salvar o modelo treinado
def save_model(model: LinearRegression, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(model, f)

# funcao para avalair o modelo
def evaluate(model:LinearRegression, y:np.ndarray, x:np.ndarray):
    pred = model.predict(x)
    r2 = r2_score(y, pred)
    logger.info(f"R² Score: {r2:.4f}")
    return r2

if __name__ == "__main__":
    # carregar os dados
    df = read_dataset(path="data/heat_exchanger.db")

    # treinar o modelo
    x = df['day_index'].values.reshape(-1, 1)
    y = df['heat_efficiency'].values
    model = train(x, y)

    # avaliar o modelo
    evaluate(model, y, x)

    # salvar o modelo treinado
    save_model(model, path = "artifacts/heat_efficiency_model.pkl")
    logger.info("Modelo treinado e salvo com sucesso!")