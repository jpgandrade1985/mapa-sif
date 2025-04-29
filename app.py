import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados geolocalizados
df_pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
df_estabelecimentos = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

df_pessoas = df_pessoas.dropna(subset=["latitude", "longitude"])
df_estabelecimentos = df_estabelecimentos.dropna(subset=["latitude", "longitude"])

# Cores suaves para status
cores_status = {
    "férias": "rgba(255, 255, 0, 1.0)",       # amarelo suave
    "em atividade": "rgba(0, 255, 0, 1.0)",    # verde suave
    "licença/afastamento": "rgba(255, 0, 0, 1.0)" # vermelho suave
}

# Cores destacadas para seleção
cores_destaque = {
    "férias": "rgba(255, 255, 0, 1.0)",
    "em atividade": "rgba(0, 200, 0, 1.0)",
    "licença/afastamento": "rgba(200, 0, 0, 1.0)"
}

st.sidebar.header("Filtros")
pessoa_selecionada = st.sidebar.selectbox("Pessoa", ["Todas"] + df_pessoas['nome'].dropna().unique().tolist())
estab_selecionado = st.sidebar.selectbox("Estabelecimento", ["Todos"] + df_estabelecimentos['nome'].dropna().unique().tolist())

# Marcar os selecionados
df_pessoas['cor'] = df_pessoas['status'].map(cores_status)
df_pessoas['tamanho'] = 13

if pessoa_selecionada != "Todas":
    df_pessoas.loc[df_pessoas['nome'] == pessoa_selecionada, 'cor'] = df_pessoas.loc[df_pessoas['nome'] == pessoa_selecionada, 'status'].map(cores_destaque)
    df_pessoas.loc[df_pessoas['nome'] == pessoa_selecionada, 'tamanho'] = 15

df_estabelecimentos['forma'] = 'square'
df_estabelecimentos['cor'] = "rgba(0, 0, 255, 0.4)"  # azul suave
df_estabelecimentos['tamanho'] = 20

if estab_selecionado != "Todos":
    df_estabelecimentos.loc[df_estabelecimentos['nome'] == estab_selecionado, 'cor'] = "rgba(0, 0, 255, 1.0)"
    df_estabelecimentos.loc[df_estabelecimentos['nome'] == estab_selecionado, 'tamanho'] = 25

# Criar mapa
fig = px.scatter_mapbox(
    df_pessoas,
    lat='latitude',
    lon='longitude',
    color_discrete_sequence=["red"],  # cor será sobrescrita manualmente
    hover_name='nome',
    hover_data={'cidade': True, 'status': True, 'lotacao': True, 'latitude': False, 'longitude': False, 'cor': False},
    zoom=6,
    height=700
)

# Adicionar manualmente os marcadores
fig.update_traces(marker=dict(size=df_pessoas['tamanho'], color=df_pessoas['cor'], symbol="circle"))

# Adicionar estabelecimentos
fig.add_scattermapbox(
    lat=df_estabelecimentos['latitude'],
    lon=df_estabelecimentos['longitude'],
    mode='markers',
    marker=dict(
        size=df_estabelecimentos['tamanho'],
        color=df_estabelecimentos['cor'],
        symbol="square"
    ),
    text=df_estabelecimentos['nome'],
    hoverinfo='text'
)

# Layout do mapa
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_zoom=6,
    mapbox_center={"lat": -23.55, "lon": -46.63},  # São Paulo como centro
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.title("📍 Mapa de Pessoas e Estabelecimentos")
st.plotly_chart(fig, use_container_width=True)
