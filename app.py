import os

import requests
import streamlit as st

DEFAULT_URL = os.getenv("API_URL", "http://localhost:8080")
TIMEOUT = 10

st.set_page_config(page_title="Heat Efficiency", page_icon="🔥", layout="centered")
st.title("🔥 Heat Efficiency")
st.caption("Cliente Streamlit para a API de predição.")

with st.sidebar:
    st.header("Configuração")
    base_url = st.text_input("URL da API", value=DEFAULT_URL).rstrip("/")

    if st.button("Verificar status", use_container_width=True):
        try:
            r = requests.get(f"{base_url}/health", timeout=TIMEOUT)
            if r.ok and r.json().get("status") == "ok":
                st.success("API online")
            else:
                st.error(f"Resposta inesperada: {r.status_code}")
        except requests.RequestException as e:
            st.error(f"Falha ao conectar: {e}")

    st.divider()
    st.subheader("Versões disponíveis")
    if st.button("Listar versões", use_container_width=True):
        try:
            r = requests.get(f"{base_url}/version", timeout=TIMEOUT)
            r.raise_for_status()
            versions = r.json()
            if versions:
                for v in versions:
                    st.code(v, language="text")
            else:
                st.info("Nenhuma versão encontrada.")
        except requests.RequestException as e:
            st.error(f"Falha: {e}")


def post(endpoint: str, payload: dict) -> dict | None:
    try:
        r = requests.post(f"{base_url}{endpoint}", json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        st.error(f"Erro na requisição: {e}")
        return None


tab_eff, tab_day = st.tabs(["Predict Efficiency", "Predict Day"])

with tab_eff:
    st.subheader("POST /predict/efficiency")
    st.write("Informe o **dia** para prever a eficiência.")
    dia = st.number_input("Dia", min_value=0, value=30, step=1, key="dia_input")
    if st.button("Prever eficiência", type="primary", key="btn_eff"):
        data = post("/predict/efficiency", {"dia": int(dia)})
        if data is not None:
            if "predicao" in data:
                st.metric("Eficiência prevista", f"{data['predicao']:.4f}")
            else:
                st.warning(data.get("error", "Resposta sem campo `predicao`."))
            with st.expander("Resposta bruta"):
                st.json(data)

with tab_day:
    st.subheader("POST /predict/day")
    st.write("Informe a **eficiência** (0–100) para prever o dia.")
    eficiencia = st.number_input(
        "Eficiência",
        min_value=0.0,
        max_value=100.0,
        value=90.0,
        step=0.1,
        key="eff_input",
    )
    if st.button("Prever dia", type="primary", key="btn_day"):
        data = post("/predict/day", {"eficiencia": float(eficiencia)})
        if data is not None:
            if "day" in data:
                st.metric("Dia previsto", f"{data['day']:.4f}")
            else:
                st.warning(data.get("error", "Resposta sem campo `day`."))
            with st.expander("Resposta bruta"):
                st.json(data)
