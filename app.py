import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    'férias': 'rgba(255, 255, 0, 1.0)',         # Amarelo claro
    'em atividade': 'rgba(0, 128, 0, 1.0)',      # Verde claro
    'licença/afastamento': 'rgba(255, 0, 0, 1.0)'  # Vermelho claro
}

pessoas['cor'] = pessoas['status'].map(cores_status)
pessoas['tamanho'] = 7
pessoas['tipo'] = 'Pessoa'

empresas['cor'] = 'rgba(0, 0, 255, 1.0)'  # Azul claro
empresas['tamanho'] = 12
empresas['status'] = ''  # para compatibilizar hover
empresas['lotação'] = ''
empresas['tipo'] = 'Estabelecimento'

# Filtros na barra lateral
st.sidebar.header("Filtros")
pessoa_sel = st.sidebar.selectbox("Selecione uma pessoa", [""] + sorted(pessoas["nome"].unique()))
empresa_sel = st.sidebar.selectbox("Selecione um estabelecimento", [""] + sorted(empresas["nome"].unique()))

# Aplica filtros
pessoas_filtrado = pessoas if not pessoa_sel else pessoas[pessoas["nome"] == pessoa_sel]
empresas_filtrado = empresas if not empresa_sel else empresas[empresas["nome"] == empresa_sel]

# Junta os dados
df_mapa = pd.concat([pessoas_filtrado, empresas_filtrado], ignore_index=True)

# Centro do mapa
center_lat = -23.5489
center_lon = -46.6388

# Criação do mapa com go.Scattermapbox
fig = go.Figure()

for _, row in df_mapa.iterrows():
    fig.add_trace(go.Scattermapbox(
        lat=[row["latitude"]],
        lon=[row["longitude"]],
        mode="markers",
        marker=dict(
            size=row["tamanho"],
            color=row["cor"],
            symbol="square" if row["tipo"] == "Estabelecimento" else "circle"
        ),
        hovertemplate=(
            f"<b>{row['nome']}</b><br>"
            f"Cidade: {row.get('cidade', '')}<br>"
            f"Status: {row.get('status', '')}<br>"
            f"Lotação: {row.get('lotação', '')}<extra></extra>"
        )
    ))

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox=dict(
        center=dict(lat=center_lat, lon=center_lon),
        zoom=10
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)
