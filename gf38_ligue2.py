from ics import Calendar, Event
import requests
from datetime import datetime
from config import HEADERS

# --- CONFIGURATION ---
TEAM_ID = 101       # GF38
SEASON = 2024       # Exemple, adapter si nécessaire

url = "https://v3.football.api-sports.io/fixtures"
params = {
    "team": TEAM_ID,
    "season": SEASON
    # PAS de filtre "league", pour prendre toutes les compétitions
}

print(">>> Envoi de la requête API...")
response = requests.get(url, headers=HEADERS, params=params)

# Vérification de la réponse
if response.status_code != 200:
    print("Erreur API :", response.status_code)
    print(response.text)
    exit(1)

data = response.json()
fixtures = data.get("response", [])
print(f"Nombre total de matchs récupérés : {len(fixtures)}")

if len(fixtures) == 0:
    print("Aucun match trouvé pour cette équipe. Vérifie la saison ou l'ID de l'équipe.")
    exit(0)

# --- Création du calendrier ---
cal = Calendar()

for match in fixtures:
    try:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        date_str = match["fixture"]["date"]

        # Convertir la date en datetime
        event_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

        # Créer l'événement
        event = Event()
        event.name = f"{home} – {away}"

        event.begin = event_date
        event.duration = {"hours": 2}

        # Ajouter le lieu si disponible
        venue = match["fixture"].get("venue", {}).get("name", "")
        if venue:
            event.location = venue

        # Ajouter la compétition dans la description
        competition = match["league"]["name"]
        event.description = f"Compétition : {competition}"

        cal.events.add(event)

        print(f"Match ajouté : {home} vs {away} ({competition}) le {event_date}")

    except Exception as e:
        print("Erreur lors de la création de l'événement :", e)

# --- Sauvegarde dans output/gf38.ics ---
output_file = "output/gf38.ics"
with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(cal)

print(f">>> Calendrier généré avec {len(cal.events)} événements : {output_file}")