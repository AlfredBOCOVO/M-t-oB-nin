@echo off
REM Aller dans le dossier du script
cd /d "%~dp0"

REM Créer l'environnement virtuel s'il n'existe pas
if not exist venv (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer et installer les dépendances
call venv\Scripts\activate
pip install -r requirements.txt

REM Lancer l'application
python -m src.main
pause