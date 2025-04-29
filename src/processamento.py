import pandas as pd
from .geocoding import obter_coordenadas_por_cep

def carregar_dados_com_coordenadas(path_pessoas, path_estabelecimentos):
    pessoas = pd.read_excel(path_pessoas)
    estabelecimentos = pd.read_excel(path_estabelecimentos)

    pessoas[['latitude', 'longitude', 'cidade']] = pessoas['CEP residencial'].apply(obter_coordenadas_por_cep)
    estabelecimentos[['latitude', 'longitude']] = estabelecimentos['CEP'].apply(lambda cep: obter_coordenadas_por_cep(cep)[:2])

    return pessoas, estabelecimentos
