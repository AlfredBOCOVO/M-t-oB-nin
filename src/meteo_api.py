import requests
import time

class MeteoAPI:
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}  # Cache pour éviter trop de requêtes

    def obtenir_coordonnees(self, ville_nom):
        """Obtenir les coordonnées GPS d'une ville"""
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={ville_nom}&count=1&language=fr&format=json"
            geo_resp = self.session.get(geo_url, timeout=10)
            geo_data = geo_resp.json()

            if not geo_data.get("results"):
                return None, None, None

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            pays = geo_data["results"][0].get("country", "")
            return lat, lon, pays
        except Exception as e:
            print(f"Erreur géocodage : {e}")
            return None, None, None

    def recuperer_donnees(self, ville_nom, force=False):
        """Récupère les données météo avec cache"""
        if not force and ville_nom in self.cache:
            # Vérifier si le cache est récent (moins de 10 minutes)
            if time.time() - self.cache[ville_nom]["timestamp"] < 600:
                print(f"📦 Utilisation des données en cache pour {ville_nom}")
                return self.cache[ville_nom]["data"]

        try:
            lat, lon, pays = self.obtenir_coordonnees(ville_nom)
            if lat is None: return None

            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "hourly": "relativehumidity_2m,pressure_msl" # On demande humidité et pression
            }
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()

            current = data.get("current_weather", {})
            hourly = data.get("hourly", {})

            # Extraction sécurisée des données horaires (index 0 = heure actuelle)
            humidite = hourly.get("relativehumidity_2m", [None])[0]
            pression = hourly.get("pressure_msl", [None])[0]

            resultat = {
                "nom": ville_nom,
                "pays": pays,
                "temperature": current.get("temperature"),
                "vitesse_vent": current.get("windspeed"),
                "humidite": humidite,
                "pression": pression, # Maintenant on a la vraie pression !
                "latitude": lat,
                "longitude": lon
            }

            # Mise en cache
            self.cache[ville_nom] = {
                "timestamp": time.time(),
                "data": resultat
            }

            return resultat

        except requests.exceptions.Timeout:
            print(f"⏰ Timeout - La requête a pris trop de temps pour {ville_nom}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"🔌 Erreur de connexion - Vérifie ta connexion Internet")
            return None
        except Exception as e:
            print(f"❌ Erreur inattendue pour {ville_nom} : {e}")
            return None