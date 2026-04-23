import matplotlib.pyplot as plt

class Statistiques:
    @staticmethod
    def moyenne_temperature(villes):
        temps = [v.temperature for v in villes if v.temperature is not None]
        return sum(temps) / len(temps) if temps else 0

    @staticmethod
    def ville_plus_chaude(villes):
        villes_valides = [v for v in villes if v.temperature is not None]
        if not villes_valides:
            return None
        return max(villes_valides, key=lambda v: v.temperature)

    @staticmethod
    def ville_plus_froide(villes):
        villes_valides = [v for v in villes if v.temperature is not None]
        if not villes_valides:
            return None
        return min(villes_valides, key=lambda v: v.temperature)

    @staticmethod
    def comparer_villes(villes):
        if not villes:
            return None
        plus_chaude = Statistiques.ville_plus_chaude(villes)
        plus_froide = Statistiques.ville_plus_froide(villes)
        return {
            "plus_chaude": plus_chaude.nom if plus_chaude else "N/A",
            "temp_plus_chaude": plus_chaude.temperature if plus_chaude else 0,
            "plus_froide": plus_froide.nom if plus_froide else "N/A",
            "temp_plus_froide": plus_froide.temperature if plus_froide else 0,
            "moyenne": round(Statistiques.moyenne_temperature(villes), 2)
        }

    @staticmethod
    def generer_graphique(villes):
        """Génère un graphique à barres des températures"""
        if not villes:
            print("Aucune donnée pour le graphique")
            return
        
        noms = [v.nom for v in villes if v.temperature is not None]
        temps = [v.temperature for v in villes if v.temperature is not None]
        
        if not noms:
            print("Aucune température valide")
            return
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(noms, temps, color=['red' if t > 25 else 'orange' if t > 15 else 'blue' for t in temps])
        plt.xlabel('Villes')
        plt.ylabel('Température (°C)')
        plt.title('Comparaison des températures')
        plt.xticks(rotation=45, ha='right')
        
        # Ajouter les valeurs sur les barres
        for bar, temp in zip(bars, temps):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{temp}°C', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()