import pandas as pd
import streamlit as st
import plotly.express as px

# Leitura dos arquivos
df_pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
df_estabelecimentos = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

# Adiciona colunas faltantes aos estabelecimentos para manter consistência
df_estabelecimentos["status"] = "Estabelecimento"
df_estabelecimentos["lotação"] = ""
df_estabelecimentos["cor"] = "blue"

# Mapeamento de cores para pessoas com base no status
mapa_cores = {
    "férias": "yellow",
    "em atividade": "green",
    "licença/afastamento": "red"
}
df_pessoas["cor"] = df_pessoas["status"].map(mapa_cores)

# Filtros da barra lateral
st.sidebar.title("Filtros")
pessoa_sel = st.sidebar.selectbox("Selecione uma pessoa:", ["Todas"] + sorted(df_pessoas["nome"].dropna().unique()))
estab_sel = st.sidebar.selectbox("Selecione um estabelecimento:", ["Todos"] + sorted(df_estabelecimentos["nome"].dropna().unique()))

# Aplicar filtros
if pessoa_sel != "Todas":
    df_pessoas_plot = df_pessoas[df_pessoas["nome"] == pessoa_sel]
else:
    df_pessoas_plot = df_pessoas.copy()

if estab_sel != "Todos":
    df_estab_plot = df_estabelecimentos[df_estabelecimentos["nome"] == estab_sel]
else:
    df_estab_plot = df_estabelecimentos.copy()

# Junta dados
df_plot = pd.concat([df_pessoas_plot, df_estab_plot], ignore_index=True)

# Verificação de colunas obrigatórias
colunas_necessarias = ['nome', 'cidade', 'status', 'lotação', 'latitude', 'longitude', 'cor']
missing = [col for col in colunas_necessarias if col not in df_plot.columns]
if missing:
    st.error(f"Erro: colunas ausentes no dataframe: {missing}")
    st.stop()

# Criar o mapa
fig = px.scatter_mapbox(
    df_plot,
    lat="latitude",
    lon="longitude",
    hover_name="nome",
    hover_data={"cidade": True, "status": True, "lotação": True},
    color_discrete_sequence=df_plot["cor"].tolist(),
    zoom=10,
    height=700
)

# Estilo mais limpo e sem legenda
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=10,
    mapbox_center={"lat": df_plot["latitude"].mean(), "lon": df_plot["longitude"].mean()},
    margin={"r":0,"t":0,"l":0,"b":0},
    showlegend=False
)

# Exibe o mapa
st.title("Mapa Interativo de Pessoas e Estabelecimentos")
st.plotly_chart(fig, use_container_width=True)
