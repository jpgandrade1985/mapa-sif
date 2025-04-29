import streamlit as st
import pandas as pd
import plotly.express as px

# ---- CONFIGURAÇÕES INICIAIS ----
st.set_page_config(layout="wide", page_title="Mapa Interativo de Pessoas e Estabelecimentos")

# ---- CARREGAR DADOS ----
df_pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
df_estabs = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

# ---- FILTROS SIDEBAR ----
st.sidebar.title("🎯 Filtros")

pessoa_selecionada = st.sidebar.selectbox("Selecione uma pessoa", ["Todas"] + df_pessoas["nome"].tolist())
estab_selecionado = st.sidebar.selectbox("Selecione um estabelecimento", ["Todos"] + df_estabs["nome"].tolist())

# ---- APLICAR FILTROS ----
df_pessoas_plot = df_pessoas.copy()
df_estabs_plot = df_estabs.copy()

highlight_pessoa = None
highlight_estab = None

if pessoa_selecionada != "Todas":
    highlight_pessoa = df_pessoas[df_pessoas["nome"] == pessoa_selecionada]
    df_pessoas_plot = df_pessoas_plot[df_pessoas_plot["nome"] != pessoa_selecionada]

if estab_selecionado != "Todos":
    highlight_estab = df_estabs[df_estabs["nome"] == estab_selecionado]
    df_estabs_plot = df_estabs_plot[df_estabs_plot["nome"] != estab_selecionado]

# ---- CORES PARA STATUS ----
cores = {
    "férias": "rgba(255, 255, 0, 0.4)",           # amarelo claro
    "em atividade": "rgba(0, 255, 0, 0.4)",       # verde claro
    "licença/afastamento": "rgba(255, 0, 0, 0.4)" # vermelho claro
}

# ---- CRIAR FIGURA PLOTLY ----
fig = px.scatter_mapbox(
    df_pessoas_plot,
    lat="latitude",
    lon="longitude",
    color="status",
    color_discrete_map=cores,
    hover_name="nome",
    hover_data=["cidade", "status", "lotação"],
    zoom=6,
    height=700,
    size_max=5
)

# Adiciona os estabelecimentos como quadrados azuis
fig.add_scattermapbox(
    lat=df_estabs_plot["latitude"],
    lon=df_estabs_plot["longitude"],
    mode="markers",
    marker=dict(size=12, symbol="square", color="rgba(0, 0, 255, 0.4)"),
    name="Estabelecimentos",
    text=df_estabs_plot["nome"],
    hoverinfo="text"
)

# Destaques com cores vivas
if highlight_pessoa is not None:
    fig.add_scattermapbox(
        lat=highlight_pessoa["latitude"],
        lon=highlight_pessoa["longitude"],
        mode="markers",
        marker=dict(size=14, color="green"),
        name="Pessoa Selecionada",
        text=highlight_pessoa["nome"],
        hoverinfo="text"
    )

if highlight_estab is not None:
    fig.add_scattermapbox(
        lat=highlight_estab["latitude"],
        lon=highlight_estab["longitude"],
        mode="markers",
        marker=dict(size=18, symbol="square", color="blue"),
        name="Estabelecimento Selecionado",
        text=highlight_estab["nome"],
        hoverinfo="text"
    )

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# ---- MOSTRAR MAPA ----
st.title("🗺️ Mapa de Pessoas e Estabelecimentos")
st.plotly_chart(fig, use_container_width=True)
