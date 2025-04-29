import streamlit as st
from src.processamento import carregar_dados_com_coordenadas
from src.mapa import criar_mapa
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.sidebar.title("Filtros")
path_pessoas = "data/pessoas.xlsx"
path_estabelecimentos = "data/estabelecimentos.xlsx"

pessoas, estabelecimentos = carregar_dados_com_coordenadas(path_pessoas, path_estabelecimentos)

nomes_pessoas = pessoas['nome'].dropna().unique().tolist()
nomes_estabelecimentos = estabelecimentos['nome'].dropna().unique().tolist()

pessoa_selecionada = st.sidebar.selectbox("Selecionar Pessoa", [None] + nomes_pessoas)
estabelecimento_selecionado = st.sidebar.selectbox("Selecionar Estabelecimento", [None] + nomes_estabelecimentos)

mapa = criar_mapa(pessoas, estabelecimentos, pessoa_selecionada, estabelecimento_selecionado)

folium_static = components.html(mapa._repr_html_(), height=700)
