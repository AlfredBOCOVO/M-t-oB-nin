import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.meteo_api import MeteoAPI
from src.ville import Ville
from src.statistiques import Statistiques

def test_api():
    print("Test de l'API...")
    api = MeteoAPI()
    donnees = api.recuperer_donnees("Paris")
    if donnees:
        print(f"✓ Paris : {donnees['temperature']}°C")
    else:
        print("✗ Échec de l'API")

def test_statistiques():
    print("\nTest des statistiques...")
    v1 = Ville("Paris")
    v1.temperature = 15
    v2 = Ville("London")
    v2.temperature = 12
    
    stats = Statistiques.comparer_villes([v1, v2])
    print(f"✓ Moyenne : {stats['moyenne']}°C")
    print(f"✓ Plus chaude : {stats['plus_chaude']}")

if __name__ == "__main__":
    test_api()
    test_statistiques()