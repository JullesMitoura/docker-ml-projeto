import os
import pickle
import argparse
from functools import lru_cache
from src.utils.logger import get_logger
from src.utils.versioning import resolve_version, list_versions
import numpy as np
from dotenv import load_dotenv


load_dotenv(override=True)
MODEL_PATH = os.getenv("MODEL_PATH")

logger = get_logger(__name__)
def load_model(model_path):
    logger.info("Carregando o modelo...")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    r2 = model['metrics']
    logger.info(f"R² Score do modelo carregado: {r2:.4f}")
    logger.info(f"Descrição do modelo: {model['description']}")
    model = model['model']
    return model


@lru_cache(maxsize=1)
def get_model():
    return load_model(resolve_version(None))

def predict_eff(model, x):
    x_array = np.array(x).reshape(1, -1)  # Reshape para garantir que seja um array 2D
    logger.info("Realizando predição de eficiencia...")
    res = model.predict(x_array)
    logger.info(f"Dia {x} | eficiência: {res[0]}.")
    return float(res[0])

def predict_data(model, y):
    coef = model.coef_
    intercept = model.intercept_
    # y = a x + b
    # x = (y - b) / a
    dia = (y - intercept) / coef[0]

    logger.info(f"Predição: eficiência {y} | dia {dia}.")
    return dia

def show_models():
    list_models = list_versions()
    for models in list_models:
        print(models)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--efficiency', type=int)
    group.add_argument('--data', type=float)
    parser.add_argument('--version', type=str, default=None)
    parser.add_argument('--list', action='store_true') # pode ou nao existir

    args = parser.parse_args()

    if args.list:
        show_models()
    else:
        model_path = resolve_version(args.version)
        model = load_model(model_path)
        if args.efficiency is not None:
            predict_eff(model, args.efficiency)
        elif args.data is not None:
            predict_data(model, args.data)