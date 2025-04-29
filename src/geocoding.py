from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

# Inicializa o geocoder
geolocator = Nominatim(user_agent="geo_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Função para extrair dados do endereço
def get_location_info(cep):
    try:
        location = geocode(cep + ", Brasil")
        if location:
            cidade = location.raw['address'].get('city', '') or \
                     location.raw['address'].get('town', '') or \
                     location.raw['address'].get('village', '')
            return pd.Series([location.latitude, location.longitude, cidade])
    except Exception as e:
        print(f"Erro no CEP {cep}: {e}")
    return pd.Series([None, None, None])

# Processar pessoas
df_pessoas = pd.read_excel("pessoas.xlsx")
df_pessoas[['latitude', 'longitude', 'cidade']] = df_pessoas['CEP residencial'].apply(get_location_info)
df_pessoas.to_excel("pessoas_geolocalizadas.xlsx", index=False)

# Processar estabelecimentos
df_estab = pd.read_excel("estabelecimentos.xlsx")
df_estab[['latitude', 'longitude', 'cidade']] = df_estab['CEP'].apply(get_location_info)
df_estab.to_excel("estabelecimentos_geolocalizados.xlsx", index=False)
