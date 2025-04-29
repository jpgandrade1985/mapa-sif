import pandas as pd
import streamlit as st
import plotly.express as px

# Leitura dos arquivos
df_pessoas = pd.read_excel("pessoas_geolocalizadas.xlsx")
df_estabelecimentos = pd.read_excel("estabelecimentos_geolocalizados.xlsx")

# Filtros na barra lateral
st.sidebar.title("Filtros")
filtro_pessoa = st.sidebar.selectbox(
    "Selecione uma pessoa:", ["Todas"] + sorted(df_pessoas["nome"].dropna().unique())
)
filtro_estab = st.sidebar.selectbox(
    "Selecione um estabelecimento:", ["Todos"] + sorted(df_estabelecimentos["nome"].dropna().unique())
)

# Aplicando filtros
if filtro_pessoa != "Todas":
    df_pessoas_plot = df_pessoas[df_pessoas["nome"] == filtro_pessoa]
else:
    df_pessoas_plot = df_pessoas.copy()

if filtro_estab != "Todos":
    df_estabelecimentos_plot = df_estabelecimentos[df_estabelecimentos["nome"] == filtro_estab]
else:
    df_estabelecimentos_plot = df_estabelecimentos.copy()

# Cores por status
cores_status = {
    "férias": "yellow",
    "em atividade": "green",
    "licença/afastamento": "red"
}
df_pessoas_plot["cor"] = df_pessoas_plot["status"].map(cores_status)
df_estabelecimentos_plot["cor"] = "blue"  # cor fixa

# Concatenando os dois conjuntos de dados
df_plot = pd.concat([df_pessoas_plot, df_estabelecimentos_plot], ignore_index=True)

# Criando o mapa
fig = px.scatter_mapbox(
    df_plot,
    lat="latitude",
    lon="longitude",
    hover_name="nome",
    hover_data=["cidade", "status", "lotação"],
    color_discrete_sequence=df_plot["cor"],
    zoom=10,
    height=700
)

# Estilo limpo do mapa
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=10,
    mapbox_center={
        "lat": df_plot["latitude"].mean(),
        "lon": df_plot["longitude"].mean()
    },
    margin={"r":0,"t":0,"l":0,"b":0},
    showlegend=False  # remove 'trace 0', etc.
)

# Exibindo o mapa
st.title("Mapa Interativo de Pessoas e Estabelecimentos")
st.plotly_chart(fig, use_container_width=True)
