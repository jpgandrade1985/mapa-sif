import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Pessoas e Estabelecimentos")

# Carrega os dados
pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
empresas = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

# Conversão e limpeza
for df in [pessoas, empresas]:
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df.dropna(subset=["latitude", "longitude"], inplace=True)

# Cores suaves padrão por status
cores_suaves = {
    'férias': 'rgba(255, 255, 0, 0.7)',       # amarelo claro
    'em atividade': 'rgba(0, 128, 0, 0.7)',   # verde claro
    'licença/afastamento': 'rgba(255, 0, 0, 0.7)'  # vermelho claro
}

# Cores destacadas
cores_vivas = {
    'férias': 'yellow',
    'em atividade': 'green',
    'licença/afastamento': 'red'
}

# Atribui cor e tamanho padrão
pessoas['cor'] = pessoas['status'].map(cores_suaves)
pessoas['tamanho'] = 4
empresas['cor'] = 'rgba(0, 0, 255, 0.7)'  # azul claro
empresas['tamanho'] = 12

# Filtros
st.sidebar.header("Filtros")
pessoa_selecionada = st.sidebar.selectbox("Selecione uma pessoa (ou nenhuma)", [""] + sorted(pessoas["nome"].unique()))
empresa_selecionada = st.sidebar.selectbox("Selecione um estabelecimento (ou nenhum)", [""] + sorted(empresas["nome"].unique()))

# Destaca seleção se houver
if pessoa_selecionada:
    pessoas.loc[pessoas["nome"] == pessoa_selecionada, "cor"] = pessoas.loc[pessoas["nome"] == pessoa_selecionada, "status"].map(cores_vivas)
    pessoas.loc[pessoas["nome"] == pessoa_selecionada, "tamanho"] = 6

if empresa_selecionada:
    empresas.loc[empresas["nome"] == empresa_selecionada, "cor"] = "blue"
    empresas.loc[empresas["nome"] == empresa_selecionada, "tamanho"] = 14

# Junta os dados
df_mapa = pd.concat([pessoas, empresas], ignore_index=True)

# Define o centro do mapa
center = {
    "lat": -23.5489,
    "lon": -46.6388
}

# Mapa com plotly express
fig = px.scatter_mapbox(
    df_mapa,
    lat="latitude",
    lon="longitude",
    hover_name="nome",
    hover_data=["cidade", "status", "lotacao"],
    color="cor",
    size="tamanho",
    size_max=20,
    zoom=10,
    center=center
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False,
    dragmode='zoom'
)

# Mostra o gráfico
st.plotly_chart(fig, use_container_width=True)
