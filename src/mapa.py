import folium
from folium.plugins import MarkerCluster

def criar_mapa(pessoas, estabelecimentos, pessoa_selecionada=None, estabelecimento_selecionado=None):
    mapa = folium.Map(location=[-15.78, -47.93], zoom_start=5)
    cluster = MarkerCluster().add_to(mapa)

    cores_status = {
        'férias': '#FFD70080',
        'em atividade': '#00800080',
        'licença/afastamento': '#FF000080'
    }

    cores_destaque = {
        'férias': '#FFD700',
        'em atividade': '#008000',
        'licença/afastamento': '#FF0000'
    }

    for _, row in estabelecimentos.iterrows():
        cor = 'blue' if row['nome'] != estabelecimento_selecionado else 'darkblue'
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['nome'],
            icon=folium.Icon(color=cor, icon='building', prefix='fa')
        ).add_to(mapa)

    for _, row in pessoas.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            cor = cores_status.get(row['status'], 'gray')
            cor_destaque = cores_destaque.get(row['status'], 'black')
            cor_final = cor_destaque if row['nome'] == pessoa_selecionada else cor
            info = f"""
            <b>Nome:</b> {row['nome']}<br>
            <b>Cidade:</b> {row.get('cidade', '')}<br>
            <b>Status:</b> {row['status']}<br>
            <b>Lotação:</b> {row['lotação']}<br>
            """
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                tooltip=folium.Tooltip(info, sticky=True),
                color=cor_final,
                fill=True,
                fill_color=cor_final,
                fill_opacity=0.7
            ).add_to(cluster)

    return mapa
