import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from src.ville import Ville
from src.meteo_api import MeteoAPI
from src.statistiques import Statistiques

class Application:
    FICHIER_HISTORIQUE = os.path.join("data", "historique.json")

    def __init__(self):
        self.api = MeteoAPI()
        self.villes = []
        self.historique = self.charger_historique()
        self.creer_interface()

    def charger_historique(self):
        """Charge l'historique depuis le fichier JSON au démarrage."""
        if os.path.exists(self.FICHIER_HISTORIQUE):
            try:
                with open(self.FICHIER_HISTORIQUE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def sauvegarder_historique(self):
        """Sauvegarde l'état actuel de self.historique dans le fichier JSON."""
        dossier = "data"
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            
        try:
            with open(self.FICHIER_HISTORIQUE, "w", encoding="utf-8") as f:
                json.dump(self.historique, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def rechercher_ville(self):
        nom = self.entry_ville.get().strip()
        if not nom:
            messagebox.showwarning("Attention", "Veuillez entrer un nom de ville")
            return
        
        self.status_label.config(text=f"Recherche de {nom}...", foreground="orange")
        self.root.update()
        
        donnees = self.api.recuperer_donnees(nom)
        if donnees:
            ville = Ville(donnees["nom"], donnees["pays"])
            ville.mettre_a_jour_meteo(donnees)
            self.villes.append(ville)
            
            # Mise à jour de l'historique (Bloc 4)
            self.historique.append(ville.to_dict())
            self.sauvegarder_historique()
            
            # Affichage des résultats
            resultat = f"✅ {ville.nom} ({ville.pays})\n"
            resultat += f"🌡️ Température : {ville.temperature}°C\n"
            if ville.humidite:
                resultat += f"💧 Humidité : {ville.humidite}%\n"
            if ville.pression: # Ajout de la pression corrigée plus tôt
                resultat += f"⏲️ Pression : {ville.pression} hPa\n"
            if ville.vent_vitesse:
                resultat += f"💨 Vent : {ville.vent_vitesse} km/h"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, resultat)
            self.status_label.config(text="✓ Recherche terminée", foreground="green")
            
            self.mettre_a_jour_liste_villes()
        else:
            messagebox.showerror("Erreur", f"Ville '{nom}' introuvable ou problème réseau")
            self.status_label.config(text="❌ Ville non trouvée", foreground="red")

    def comparer_villes(self):
        if len(self.villes) < 2:
            messagebox.showwarning("Attention", "Ajoutez au moins 2 villes avant de comparer")
            return
        
        stats = Statistiques.comparer_villes(self.villes)
        if stats:
            resultat = "📊 STATISTIQUES COMPARATIVES\n"
            resultat += "="*30 + "\n"
            resultat += f"🌡️ Moyenne des températures : {stats['moyenne']}°C\n"
            resultat += f"🔥 Plus chaude : {stats['plus_chaude']} ({stats['temp_plus_chaude']}°C)\n"
            resultat += f"❄️ Plus froide : {stats['plus_froide']} ({stats['temp_plus_froide']}°C)\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, resultat)
            
            if messagebox.askyesno("Graphique", "Voulez-vous voir le graphique des températures ?"):
                Statistiques.generer_graphique(self.villes)

    def afficher_historique(self):
        if not self.historique:
            messagebox.showinfo("Historique", "Aucune recherche dans l'historique")
            return
        
        resultat = "📜 HISTORIQUE (10 dernières)\n"
        resultat += "="*30 + "\n"
        # On affiche les 10 derniers éléments
        for entree in self.historique[-10:]:
            resultat += f"🏙️ {entree.get('nom')} : {entree.get('temperature')}°C\n"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, resultat)

    def vider_liste(self):
        self.villes.clear()
        self.mettre_a_jour_liste_villes()
        self.result_text.delete(1.0, tk.END)
        self.status_label.config(text="Liste de session vidée", foreground="blue")

    def mettre_a_jour_liste_villes(self):
        self.listbox_villes.delete(0, tk.END)
        for ville in self.villes:
            self.listbox_villes.insert(tk.END, f"{ville.nom} : {ville.temperature}°C")

    def creer_interface(self):
        self.root = tk.Tk()
        self.root.title("🌤️ Explorateur Météo Python")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f0f0')
        
        style = ttk.Style()
        style.theme_use('clam')
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        title_label = tk.Label(main_frame, text="🌤️ EXPLORATEUR MÉTÉO PYTHON 🌧️", 
                               font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        
        ttk.Label(search_frame, text="Nom de la ville :").pack(side=tk.LEFT, padx=5)
        self.entry_ville = ttk.Entry(search_frame, width=30)
        self.entry_ville.pack(side=tk.LEFT, padx=5)
        self.entry_ville.bind('<Return>', lambda event: self.rechercher_ville())
        
        ttk.Button(search_frame, text="🔍 Rechercher", command=self.rechercher_ville).pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="📊 Comparer", command=self.comparer_villes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📜 Historique", command=self.afficher_historique).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Vider liste", command=self.vider_liste).pack(side=tk.LEFT, padx=5)
        
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")
        
        list_frame = ttk.LabelFrame(display_frame, text="Session actuelle", padding="5")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.listbox_villes = tk.Listbox(list_frame, height=10, width=25)
        self.listbox_villes.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox_villes.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_villes.config(yscrollcommand=scrollbar.set)
        
        result_frame = ttk.LabelFrame(display_frame, text="Détails", padding="5")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.result_text = tk.Text(result_frame, height=10, width=40, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Label(main_frame, text="Prêt", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                      bg='#f0f0f0', fg='green')
        self.status_label.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

    def lancer(self):
        self.root.mainloop()