import requests
from transformers import pipeline   # utilisation d'un modèle de résumé

# création d'une instance globale du modèle de résumé
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_weather(city: str, lat: float, lon: float, current_time_str: str):
    # appel a l'API météo
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&hourly=temperature_2m"
        f"&timezone=Europe/Paris"
    )
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Erreur lors de la récupération des données météo"}

    try:
        data = response.json()
    except ValueError:
        return {"error": "Réponse API invalide"}

    # Extraction des températures et heures
    temperatures = data.get("hourly", {}).get("temperature_2m", [])
    times = data.get("hourly", {}).get("time", [])

    if not temperatures or not times:
        return {"error": "Données météo insuffisantes"}

    try:
        # trouver l'index de la date heure actuel dans la liste des temps de l'API météo
        index = times.index(current_time_str)
    except ValueError:
        return {"error": f"Aucune donnée météo pour l'heure actuelle : {current_time_str}"}

    temp_now = temperatures[index]
    phrase = f"À {current_time_str.replace('T', ' ')}, la température à {city} est de {temp_now} degrés Celsius."

    summary = summarizer(phrase, max_length=15, min_length=10, do_sample=False)
    summary_text = summary[0]["summary_text"]

    return {"resume": summary_text}
