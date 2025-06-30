# créer un router contenant la route / qui affiche la page HTML
# permet de regrouper des routes liées dans des modules séparés 
#  @app.get  = direct sur l'app principale 

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
