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
            # Étape 1 : Coordonnées
            lat, lon, pays = self.obtenir_coordonnees(ville_nom)
            if lat is None:
                return None

            # Étape 2 : Météo actuelle
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m,pressure_msl"
            }
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()

            current = data.get("current_weather", {})
            
            # Récupérer l'humidité depuis hourly (première heure)
            humidite = None
            if "hourly" in data and "relativehumidity_2m" in data["hourly"]:
                if data["hourly"]["relativehumidity_2m"]:
                    humidite = data["hourly"]["relativehumidity_2m"][0]

            resultat = {
                "nom": ville_nom,
                "pays": pays,
                "temperature": current.get("temperature"),
                "vitesse_vent": current.get("windspeed"),
                "humidite": humidite,
                "pression": None,
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