#!/bin/bash
# Aller dans le dossier du script
cd "$(dirname "$0")"

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer et lancer
source venv/bin/activate
pip install -r requirements.txt
python3 -m src.main