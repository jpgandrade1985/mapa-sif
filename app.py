import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Mapa Interativo de Pessoas e Estabelecimentos")

# Carrega os dados
pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
empresas = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

# Adicionando os dados de localização geográfica (latitude e longitude)
pessoas['latitude'] = pessoas['cep'].apply(lambda x: get_geolocation(x)['lat'])
pessoas['longitude'] = pessoas['cep'].apply(lambda x: get_geolocation(x)['lon'])
empresas['latitude'] = empresas['cep'].apply(lambda x: get_geolocation(x)['lat'])
empresas['longitude'] = empresas['cep'].apply(lambda x: get_geolocation(x)['lon'])

# Adicionando cidade
pessoas['cidade'] = pessoas['cep'].apply(lambda x: get_city(x))

# Barra lateral com filtros
st.sidebar.header('Filtros')
pessoa_selecionada = st.sidebar.selectbox('Selecione uma pessoa:', ['Todos'] + list(pessoas['nome'].unique()))
estabelecimento_selecionado = st.sidebar.selectbox('Selecione um estabelecimento:', ['Todos'] + list(empresas['nome'].unique()))

# Filtrando dados
pessoas_filtrado = pessoas.copy()
empresas_filtrado = empresas.copy()

if pessoa_selecionada not in [None, '', 'Todos']:
    pessoas_filtrado = pessoas[pessoas['nome'] == pessoa_selecionada]

if estabelecimento_selecionado not in [None, '', 'Todos']:
    empresas_filtrado = empresas[df_estabs['nome'] == estabelecimento_selecionado]

# Ajustando o centro do mapa
center_lat = pessoas_filtrado['latitude'].mean()
center_lon = pessoas_filtrado['longitude'].mean()

# Adicionando as cores para cada status
status_cor = {
    'férias': 'rgba(255, 255, 0, 0.7)',  # Amarelo suave
    'em atividade': 'rgba(0, 255, 0, 0.7)',  # Verde suave
    'licença/afastamento': 'rgba(255, 0, 0, 0.7)'  # Vermelho suave
}

pessoas_filtrado['cor'] = pessoas_filtrado['status'].map(status_cor)
empresas_filtrado['cor'] = 'rgba(0, 0, 255, 0.7)'  # Cor fixa para os estabelecimentos

# Criando o mapa
fig = px.scatter_mapbox(
    df_pessoas_filtrado.append(empresas_filtrado),
    lat="latitude",
    lon="longitude",
    color="cor",
    hover_name="nome",
    hover_data=["cidade", "status", "lotação"],
    title="Mapa de Pessoas e Estabelecimentos",
    color_continuous_scale="Viridis",
    size_max=10,
    zoom=10
)

# Removendo a legenda e configurando o mapa
fig.update_layout(
    mapbox_style="carto-positron",  # Mapa mais limpo
    mapbox=dict(
        center=dict(lat=center_lat, lon=center_lon),
        zoom=10
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False  # Removendo a legenda
)

# Exibindo o mapa
st.plotly_chart(fig)
