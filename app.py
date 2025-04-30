import pandas as pd
import streamlit as st
import plotly.express as px

# Leitura dos dados
df_pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
df_estab = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

# Adiciona colunas consistentes
df_estab["status"] = "Estabelecimento"
df_estab["lotação"] = ""

# Filtros na barra lateral
st.sidebar.title("Filtros")
pessoa_sel = st.sidebar.selectbox("Selecione uma pessoa:", ["Todas"] + sorted(df_pessoas["nome"].dropna().unique()))
estab_sel = st.sidebar.selectbox("Selecione um estabelecimento:", ["Todos"] + sorted(df_estab["nome"].dropna().unique()))

# Aplicar filtros
df_pessoas_plot = df_pessoas if pessoa_sel == "Todas" else df_pessoas[df_pessoas["nome"] == pessoa_sel]
df_estab_plot = df_estab if estab_sel == "Todos" else df_estab[df_estab["nome"] == estab_sel]

# Junta os dados filtrados
df_plot = pd.concat([df_pessoas_plot, df_estab_plot], ignore_index=True)

# Verifica colunas obrigatórias
obrigatorias = ["nome", "cidade", "status", "lotação", "latitude", "longitude"]
faltando = [col for col in obrigatorias if col not in df_plot.columns]
if faltando:
    st.error(f"Colunas faltando: {faltando}")
    st.stop()

# Remove linhas com coordenadas ausentes
df_plot = df_plot.dropna(subset=["latitude", "longitude"])

# Define símbolo e tamanho
df_plot["tamanho"] = df_plot["status"].apply(lambda x: 20 if x == "Estabelecimento" else 12)

fig = px.scatter_mapbox(
    df_plot,
    lat="latitude",
    lon="longitude",
    hover_name="nome",
    hover_data={"cidade": True, "status": True, "lotação": True},
    color="status",
    symbol="status",
    size="tamanho",
    size_max=20,
    zoom=5,
    height=700,
    color_discrete_map={
        "Estabelecimento": "blue",
        "férias": "yellow",
        "em atividade": "green",
        "licença/afastamento": "red"
    },
    symbol_map={
        "Estabelecimento": "square",
        "férias": "circle",
        "em atividade": "circle",
        "licença/afastamento": "circle"
    }
)

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_center={"lat": df_plot["latitude"].mean(), "lon": df_plot["longitude"].mean()},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False
)

st.title("Mapa Interativo de Pessoas e Estabelecimentos")
st.plotly_chart(fig, use_container_width=True)
