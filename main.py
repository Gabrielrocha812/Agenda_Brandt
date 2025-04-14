from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ldap3 import Server, Connection, NTLM, ALL
from Crypto.Hash import MD4
import hashlib
import models
from database import engine

#Inicio Padroes FastAPI
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

hashlib.md4 = lambda: MD4.new()

LDAP_SERVER = "ldap://10.2.8.24"
LDAP_DOMAIN = "brandt.local"
LDAP_BASE_DN = "dc=brandt,dc=local"

#Fim Padroes FastAPI

#Inicio Funções
def authenticate_with_ad(username: str, password: str):
    user_dn = f"{LDAP_DOMAIN}\\{username}"

    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(
            server,
            user=user_dn,
            password=password,
            authentication=NTLM,
        )

        if conn.bind():
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao autenticar no AD: {e}")
        return False

def is_admin(username: str):
    return username.lower() == "gabriel.rocha"

def get_redirect_url(username: str) -> str:
    user_routes = {
        "gabriel.rocha" : "/Arqueologia",
        "vleite" : "/Arqueologia",
        "rodrigo.pessoa" : "/Biodiversidade",
        "tlima" : "/Espeleologia",
        "llacerda" : "/Geointeligencia",
        "agobira" : "/Humanidades",
        "vinicius.santos" : "/MeioFisico",
        "clisboa" : "/Modelagens",
        "lthays" : "/Gerencia",
        "msantos" : "/Gerencia"
    }

    return user_routes.get(username.lower(), "/Info")
#Fim Funções

@app.get("/")
async def login(request: Request):
    error_message = request.query_params.get('error')
    success_message = request.query_params.get('success')
    return templates.TemplateResponse(
        "login.html", {"request": request, "error_message": error_message, "success_message": success_message}
    )

@app.post("/logar")
async def login(username: str = Form(...), password: str = Form(...)):
    if authenticate_with_ad(username, password):
        redirect_url = get_redirect_url(username)
        return RedirectResponse(url=redirect_url, status_code=303)
    else:
        return RedirectResponse(url="/?error=Credenciais inválidas", status_code=303)


