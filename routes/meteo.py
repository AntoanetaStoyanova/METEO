from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils import get_lat_lon  # recuperer les coordonnées GPS d'une ville importé depuis utils.py
from summarizer import summarize_weather
from datetime import datetime, timezone, timedelta # gérer la date et l'heure actuel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/meteo_resume_by_city", response_class=HTMLResponse)
def meteo_resume_by_city(request: Request, city: str = Form(...)):
    # recupération des coordonnées GPS
    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Ville introuvable"})

    # calcul de l'heure actuel ( l'api meteo )
    now = datetime.now(timezone.utc) + timedelta(hours=2)
    current_time_str = now.strftime("%Y-%m-%dT%H:00")

    #appeler l'API météo , extraction de la température et créer un résumé
    result = summarize_weather(city, lat, lon, current_time_str)

    if "error" in result:
        return templates.TemplateResponse("index.html", {"request": request, "error": result["error"]})

    return templates.TemplateResponse("index.html", {
        "request": request,
        "city": city,
        "resume": result["resume"]
    })
