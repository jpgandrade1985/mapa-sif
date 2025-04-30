import pandas as pd
import streamlit as st
import plotly.express as px

# Leitura dos arquivos
df_pessoas = pd.read_excel("dados/pessoas_geolocalizadas.xlsx")
df_estabelecimentos = pd.read_excel("dados/estabelecimentos_geolocalizados.xlsx")

# Adiciona colunas faltantes aos estabelecimentos para manter consistência
df_estabelecimentos["status"] = "Estabelecimento"
df_estabelecimentos["lotação"] = ""

# Junta os dois dataframes
df_total = pd.concat([df_pessoas, df_estabelecimentos], ignore_index=True)

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

# Junta dados filtrados
df_plot = pd.concat([df_pessoas_plot, df_estab_plot], ignore_index=True)

# Define tamanho dos marcadores
df_plot["tamanho"] = df_plot["status"].apply(lambda x: 20 if x == "Estabelecimento" else 12)

# Criar o mapa
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

# Ajustes no layout
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_center={"lat": df_plot["latitude"].mean(), "lon": df_plot["longitude"].mean()},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False
)

# Exibe o mapa
st.title("Mapa Interativo de Pessoas e Estabelecimentos")
st.plotly_chart(fig, use_container_width=True)
