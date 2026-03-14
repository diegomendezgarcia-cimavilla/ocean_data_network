import streamlit as st
import pandas as pd
import pydeck as pdk
import os

DATA_PATH = "data/pescas.csv"

st.set_page_config(page_title="Blue Tech Fishing Dashboard", layout="wide")

st.title("🌊 Blue Tech Fishing Intelligence")
st.write("Dashboard de datos de pesca artesanal")

# asegurar carpeta
os.makedirs("data", exist_ok=True)

columns = ["fecha","hora","zona","lat","lon","especie","cantidad"]

# cargar datos
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    df = pd.DataFrame(columns=columns)

# -------------------------
# KPIs
# -------------------------

st.header("📊 Indicadores")

col1, col2, col3 = st.columns(3)

col1.metric("Total capturas", len(df))

if not df.empty:
    col2.metric("Especies registradas", df["especie"].nunique())
    col3.metric("Zonas de pesca", df["zona"].nunique())
else:
    col2.metric("Especies registradas", 0)
    col3.metric("Zonas de pesca", 0)

# -------------------------
# dataset
# -------------------------

st.header("📋 Dataset")

if df.empty:
    st.warning("No hay datos todavía")
else:
    st.dataframe(df)

# descargar dataset
if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Descargar dataset",
        csv,
        "dataset_pesca_artesanal.csv",
        "text/csv",
    )

# -------------------------
# gráfico especies
# -------------------------

if not df.empty:
    st.header("🐟 Capturas por especie")

    especies = df["especie"].value_counts()

    st.bar_chart(especies)

# -------------------------
# MAPA
# -------------------------

st.header("🗺️ Mapa global de capturas")

if not df.empty and "lat" in df.columns and "lon" in df.columns:

    mapa_df = df.dropna(subset=["lat","lon"])

    if not mapa_df.empty:

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=mapa_df,
            get_position="[lon, lat]",
            get_color="[200, 30, 0, 160]",
            get_radius=3000,
        )

        view_state = pdk.ViewState(
            latitude=mapa_df["lat"].mean(),
            longitude=mapa_df["lon"].mean(),
            zoom=4,
        )

        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                map_style="mapbox://styles/mapbox/light-v9",
            )
        )

    else:
        st.info("No hay coordenadas todavía")

else:
    st.info("Añade capturas con latitud y longitud")

# -------------------------
# HEATMAP
# -------------------------

st.header("🔥 Heatmap de actividad pesquera")

if not df.empty:

    mapa_df = df.dropna(subset=["lat","lon"])

    if not mapa_df.empty:

        heat_layer = pdk.Layer(
            "HeatmapLayer",
            data=mapa_df,
            get_position="[lon, lat]",
            opacity=0.8,
        )

        view_state = pdk.ViewState(
            latitude=mapa_df["lat"].mean(),
            longitude=mapa_df["lon"].mean(),
            zoom=4,
        )

        st.pydeck_chart(
            pdk.Deck(
                layers=[heat_layer],
                initial_view_state=view_state
            )
        )
