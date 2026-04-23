class Ville:
    def __init__(self, nom, pays=""):
        self.nom = nom
        self.pays = pays
        self.temperature = None
        self.humidite = None
        self.vent_vitesse = None
        self.pression = None
        self.latitude = None
        self.longitude = None

    def mettre_a_jour_meteo(self, donnees):
        """Met à jour les attributs météo à partir du JSON parsé"""
        self.temperature = donnees.get("temperature")
        self.humidite = donnees.get("humidite")
        self.vent_vitesse = donnees.get("vitesse_vent")
        self.pression = donnees.get("pression")
        self.latitude = donnees.get("latitude")
        self.longitude = donnees.get("longitude")

    def afficher(self):
        return f"{self.nom} ({self.pays}) : {self.temperature}°C, {self.humidite}% humidité"

    def to_dict(self):
        return {
            "nom": self.nom,
            "pays": self.pays,
            "temperature": self.temperature,
            "humidite": self.humidite,
            "vent_vitesse": self.vent_vitesse,
            "pression": self.pression,
            "latitude": self.latitude,
            "longitude": self.longitude
        }