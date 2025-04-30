import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Leitura dos dados
df_pessoas = pd.read_csv("dados/pessoas_geolocalizadas.csv")
df_estab = pd.read_csv("dados/estabelecimentos_geolocalizados.csv")

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
    "Estabelecimento": "LightSkyBlue"
}

# Adiciona coluna de hover individual
df_pessoas_plot["hover"] = "Pessoa: " + df_pessoas_plot["nome"] + " (" + df_pessoas_plot["cidade"] + ")"
df_estab_plot["hover"] = "Estabelecimento: " + df_estab_plot["nome"] + " (" + df_estab_plot["cidade"] + ")"

# Identifica coordenadas duplicadas (pessoas e estabelecimentos no mesmo ponto)
coords_pessoas = set(zip(df_pessoas_plot["latitude"], df_pessoas_plot["longitude"]))
coords_estabs = set(zip(df_estab_plot["latitude"], df_estab_plot["longitude"]))
coords_comuns = coords_pessoas & coords_estabs

# Dados combinados para pontos coincidentes
df_combinado = pd.DataFrame([
    {
        "latitude": lat,
        "longitude": lon,
        "hover": "<br>".join([
            df_pessoas_plot[(df_pessoas_plot["latitude"] == lat) & (df_pessoas_plot["longitude"] == lon)]["hover"].values[0],
            df_estab_plot[(df_estab_plot["latitude"] == lat) & (df_estab_plot["longitude"] == lon)]["hover"].values[0]
        ])
    }
    for lat, lon in coords_comuns
])

# Inicia o mapa
fig = go.Figure()

# Adiciona estabelecimentos (sempre azuis claros)
fig.add_trace(go.Scattermapbox(
    lat=df_estab_plot["latitude"],
    lon=df_estab_plot["longitude"],
    mode="markers",
    marker=dict(size=20, color='LightSkyBlue'), 
    line=dict(color='MediumPurple', width=7),
    hovertext=df_estab_plot["hover"],
    hoverinfo="text",
    showlegend=False
))

# Adiciona marcadores de pessoas com cores diferentes por status
for status in df_pessoas_plot["status"].unique():
    df_status = df_pessoas_plot[df_pessoas_plot["status"] == status]
    fig.add_trace(go.Scattermapbox(
        lat=df_status["latitude"],
        lon=df_status["longitude"],
        mode="markers",
        marker=dict(size=12, color=cores.get(status, "gray"), symbol="circle"),
        hovertext=df_status["hover"],
        hoverinfo="text",
        showlegend=False
    ))



# Adiciona marcador transparente com hover combinado
if not df_combinado.empty:
    fig.add_trace(go.Scattermapbox(
        lat=df_combinado["latitude"],
        lon=df_combinado["longitude"],
        mode="markers",
        marker=dict(size=25, color="rgba(0,0,0,0)"),  # invisível
        hovertext=df_combinado["hover"],
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
