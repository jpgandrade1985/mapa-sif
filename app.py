import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Mapa Interativo de Pessoas e Estabelecimentos")

# Carrega os dados
pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
empresas = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

# Converte latitude e longitude para numérico e remove inválidos
for df in [pessoas, empresas]:
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df.dropna(subset=["latitude", "longitude"], inplace=True)

# Cores suaves por status
cores_status = {
    'férias': 'rgba(255, 255, 0, 0.4)',         # Amarelo claro
    'em atividade': 'rgba(0, 128, 0, 0.4)',      # Verde claro
    'licença/afastamento': 'rgba(255, 0, 0, 0.4)'  # Vermelho claro
}

# Atribui cor e tamanho fixo
pessoas['cor'] = pessoas['status'].map(cores_status)
pessoas['tamanho'] = 7

empresas['cor'] = 'rgba(0, 0, 255, 0.4)'  # Azul claro
empresas['tamanho'] = 12

# Filtros na barra lateral
st.sidebar.header("Filtros")
pessoa_sel = st.sidebar.selectbox("Selecione uma pessoa", [""] + sorted(pessoas["nome"].unique()))
empresa_sel = st.sidebar.selectbox("Selecione um estabelecimento", [""] + sorted(empresas["nome"].unique()))

# Aplica filtros condicionais
pessoas_filtrado = pessoas if not pessoa_sel else pessoas[pessoas["nome"] == pessoa_sel]
empresas_filtrado = empresas if not empresa_sel else empresas[empresas["nome"] == empresa_sel]

# Junta dados para o mapa
df_mapa = pd.concat([pessoas_filtrado, empresas_filtrado], ignore_index=True)

# Centro do mapa
center = {
    "lat": df_mapa["latitude"].mean(),
    "lon": df_mapa["longitude"].mean()
}

# Criação do mapa
fig = px.scatter_mapbox(
    df_mapa,
    lat="latitude",
    lon="longitude",
    hover_name="nome",
    hover_data=["cidade", "status", "lotação"],
    color="cor",
    size="tamanho",
    size_max=20,
    zoom=10,
    center=center
)

# Layout e controles do mapa
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False,
    dragmode='zoom'
)

# Exibe o mapa
st.plotly_chart(fig, use_container_width=True)
