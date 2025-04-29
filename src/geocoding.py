from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

geolocator = Nominatim(user_agent="meu_app_mapa")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def obter_coordenadas_por_cep(cep):
    try:
        localizacao = geocode({"postalcode": cep, "country": "Brazil"})
        if localizacao:
            return pd.Series([localizacao.latitude, localizacao.longitude])
        else:
            return pd.Series([None, None])
    except:
        return pd.Series([None, None])

# src/processamento.py
import pandas as pd
from .geocoding import obter_coordenadas_por_cep

def carregar_dados_com_coordenadas(path_pessoas, path_estabelecimentos):
    pessoas = pd.read_excel(path_pessoas)
    estabelecimentos = pd.read_excel(path_estabelecimentos)

    pessoas[['latitude', 'longitude']] = pessoas['CEP residencial'].apply(obter_coordenadas_por_cep)
    estabelecimentos[['latitude', 'longitude']] = estabelecimentos['CEP'].apply(obter_coordenadas_por_cep)

    return pessoas, estabelecimentos
