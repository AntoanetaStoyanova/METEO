from fastapi import FastAPI
from fastapi.templating import Jinja2Templates # gere les templates HTML 

from routes import home, meteo  # on importe nos modules de routes

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Inclure les routes dans l'app
app.include_router(home.router)
app.include_router(meteo.router)
