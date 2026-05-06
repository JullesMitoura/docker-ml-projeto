import os
import pickle
from datetime import datetime
from glob import glob

ARTIFACTS_DIR = "artifacts"
MODEL_PREFIX = "heat_efficiency_model"
TIMESTAMP_FMT = "%Y-%m-%d_%H-%M-%S"


def get_version() -> str:
    timestamp = datetime.now().strftime(TIMESTAMP_FMT)
    return os.path.join(ARTIFACTS_DIR, f"{MODEL_PREFIX}_{timestamp}.pkl")


def list_versions() -> list[str]:
    """Nomes (sem .pkl), do mais recente para o mais antigo."""
    paths = sorted(
        glob(os.path.join(ARTIFACTS_DIR, f"{MODEL_PREFIX}_*.pkl")),
        reverse=True,
    )
    return [os.path.splitext(os.path.basename(p))[0] for p in paths]


def resolve_version(version: str | None) -> str:
    if version in (None, "latest"):
        versions = list_versions()
        if not versions:
            raise FileNotFoundError(
                f"Nenhum artefato encontrado em '{ARTIFACTS_DIR}/'. "
                f"Treine um modelo primeiro (python src/train.py)."
            )
        version = versions[0]
    path = os.path.join(ARTIFACTS_DIR, f"{version}.pkl")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Versão não encontrada: '{version}'. Use --list para ver as disponíveis."
        )
    return path


def describe_versions() -> list[dict]:
    rows = []
    for name in list_versions():
        row = {"name": name, "r2": None, "description": None, "error": None}
        try:
            with open(os.path.join(ARTIFACTS_DIR, f"{name}.pkl"), "rb") as f:
                data = pickle.load(f)
            row["r2"] = data.get("metrics")
            row["description"] = data.get("description")
        except Exception as exc:
            row["error"] = str(exc)
        rows.append(row)
    return rows