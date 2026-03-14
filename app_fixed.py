import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Ruta del CSV
DATA_PATH = "data/pescas.csv"

st.set_page_config(page_title="Global Fishing Watch Artesanal", layout="wide")

st.title("🌊 Global Fishing Watch Artesanal")
st.write("Registro y visualización de capturas de pescadores artesanales")

# Crear carpeta data si no existe
os.makedirs("data", exist_ok=True)

# Inicializar dataframe vacío
columns = ["fecha","hora","zona","lat","lon","especie","cantidad"]

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    df = pd.DataFrame(columns=columns)

# --- Formulario de registro ---
st.header("Registrar una pesca")

with st.form("registro_pesca"):
    fecha = st.date_input("Fecha", value=datetime.today())
    hora = st.time_input("Hora", value=datetime.now().time())
    zona = st.text_input("Zona de pesca")
    lat = st.number_input("Latitud (opcional)", format="%.6f")
    lon = st.number_input("Longitud (opcional)", format="%.6f")
    especie = st.text_input("Especie capturada")
    cantidad = st.number_input("Cantidad aproximada", min_value=1, step=1)

    submit = st.form_submit_button("Guardar registro")

if submit:
    nuevo = pd.DataFrame(
        [[fecha, hora, zona, lat, lon, especie, cantidad]],
        columns=columns
    )

    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

    st.success("Registro guardado correctamente!")

# --- Visualización del dataset ---
st.header("📊 Datos de pesca")

if df.empty:
    st.warning("Aún no hay registros.")
else:
    st.dataframe(df)

# Métrica rápida
st.metric("Total capturas registradas", len(df))

# --- Gráfico de especies ---
if not df.empty:
    st.subheader("🐟 Capturas por especie")
    st.bar_chart(df["especie"].value_counts())

# --- Mapa interactivo ---
st.header("🗺️ Mapa de capturas")

if not df.empty and "lat" in df.columns and "lon" in df.columns:
    mapa_df = df.dropna(subset=["lat","lon"])

    if not mapa_df.empty:
        st.map(mapa_df[["lat","lon"]])
    else:
        st.info("Registra algunas capturas con coordenadas para ver el mapa.")
else:
    st.info("Registra algunas capturas con coordenadas para ver el mapa.")
