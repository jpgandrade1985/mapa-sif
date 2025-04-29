from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

geolocator = Nominatim(user_agent="meu_app_mapa")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def obter_coordenadas_por_cep(cep):
    try:
        localizacao = geocode({"postalcode": cep, "country": "Brazil"})
        if localizacao:
            cidade = localizacao.raw.get('address', {}).get('city') or \
                     localizacao.raw.get('address', {}).get('town') or \
                     localizacao.raw.get('address', {}).get('village') or ''
            return pd.Series([localizacao.latitude, localizacao.longitude, cidade])
        else:
            return pd.Series([None, None, None])
    except:
        return pd.Series([None, None, None])
