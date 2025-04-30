import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Leitura dos dados
df_pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
df_estab = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

# Adiciona colunas consistentes
df_estab["status"] = "Estabelecimento"
df_estab["lotacao"] = ""

# Filtros
st.sidebar.title("Filtros")
pessoa_sel = st.sidebar.selectbox("Selecione uma pessoa:", ["Todas"] + sorted(df_pessoas["nome"].dropna().unique()))
estab_sel = st.sidebar.selectbox("Selecione um estabelecimento:", ["Todos"] + sorted(df_estab["nome"].dropna().unique()))

df_pessoas_plot = df_pessoas if pessoa_sel == "Todas" else df_pessoas[df_pessoas["nome"] == pessoa_sel]
df_estab_plot = df_estab if estab_sel == "Todos" else df_estab[df_estab["nome"] == estab_sel]

# Verificação de colunas obrigatórias
obrigatorias = ["nome", "cidade", "status", "lotacao", "latitude", "longitude"]
for df in [df_pessoas_plot, df_estab_plot]:
    faltando = [col for col in obrigatorias if col not in df.columns]
    if faltando:
        st.error(f"Colunas faltando: {faltando}")
        st.stop()

# Remove entradas com coordenadas ausentes
df_pessoas_plot = df_pessoas_plot.dropna(subset=["latitude", "longitude"])
df_estab_plot = df_estab_plot.dropna(subset=["latitude", "longitude"])

# Mapeamento de cores
cores = {
    "em atividade": "green",
    "férias": "yellow",
    "licença/afastamento": "red",
    "Estabelecimento": "blue"
}

# Inicia o mapa
fig = go.Figure()

# Adiciona pessoas
for status in df_pessoas_plot["status"].unique():
    df_status = df_pessoas_plot[df_pessoas_plot["status"] == status]
    fig.add_trace(go.Scattermapbox(
        lat=df_status["latitude"],
        lon=df_status["longitude"],
        mode="markers",
        marker=dict(size=12, color=cores.get(status, "gray"), symbol="circle"),
        hovertext=df_status["nome"] + " (" + df_status["cidade"] + ")",
        hoverinfo="text",
        showlegend=False
    ))

# Adiciona estabelecimentos (sempre azuis e quadrados)
fig.add_trace(go.Scattermapbox(
    lat=df_estab_plot["latitude"],
    lon=df_estab_plot["longitude"],
    mode="markers",
    marker=dict(size=20, color="blue", symbol="square"),
    hovertext=df_estab_plot["nome"] + " (" + df_estab_plot["cidade"] + ")",
    hoverinfo="text",
    showlegend=False
))

# Layout do mapa
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center=dict(
        lat=pd.concat([df_pessoas_plot["latitude"], df_estab_plot["latitude"]]).mean(),
        lon=pd.concat([df_pessoas_plot["longitude"], df_estab_plot["longitude"]]).mean(),
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False
)

# Exibição
st.title("Mapa Interativo de Pessoas e Estabelecimentos")
st.plotly_chart(fig, use_container_width=True)
