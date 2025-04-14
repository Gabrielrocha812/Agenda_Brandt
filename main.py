from fastapi import  FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ldap3 import Server, Connection, NTLM, ALL
from Crypto.Hash import MD4
import hashlib

#Inicio Padroes FastAPI
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
config = {"ASSETS_ROOT": "/static/assets"}

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

def get_redirect_url(username: str) -> str:
    user_routes = {
        "gabriel.rocha" : "MeM",
        "vleite" : "Arq",
        "rodrigo.pessoa" : "Bio",
        "tlima" : "Esp",
        "llacerda" : "Geo",
        "agobira" : "Hum",
        "vinicius.santos" : "MeM",
        "clisboa" : "MeM",
        "lthays" : "Gerencia",
        "msantos" : "Gerencia"
    }

    return user_routes.get(username.lower(), "Info")

#Fim Funções

#inicio endpoints de login

@app.get("/")
async def login(request: Request):
    error_message = request.query_params.get('error')
    success_message = request.query_params.get('success')
    return templates.TemplateResponse(
        "login.html", {"request": request, "error_message": error_message, "success_message": success_message}
    )

@app.post("/logar")
async def logar(username: str = Form(...), password: str = Form(...)):
    if authenticate_with_ad(username, password):
        redirect_url = get_redirect_url(username)
        return RedirectResponse(url=redirect_url, status_code=303)
    else:
        return RedirectResponse(url="/?error=Credenciais inválidas", status_code=303)

#fim endpoints de login

#inicio endpoints agenda

@app.get("/{hub}")
async def index_hubs(
    request: Request,
    hub: str,
):
    mapa_models = {
        "Arq": ("Arq", "./Arqueologia/index.html"),
        "Bio": ("Bio", "./Biodiversidade/index.html"),
        "Esp": ("Esp", "./Espeleologia/index.html"),
        "Geo": ("Geo", "./Geo/index.html"),
        "Hum": ("Hum", "./Humanidades/index.html"),
        "MeM": ("MeM", "./mem.html"),
        "Gerencia": ("Gerencia", "./Gerencia/index.html"),
        "MF": ("MF", "./MeioFisico/index.html"),
        "Mod": ("Mod", "./Modelagens/index.html"),
    }

    model, caminho = mapa_models.get(hub, (None, None))

    if not model or not caminho:
        return {"error": f"O hub '{hub}' não é válido."}

    return templates.TemplateResponse(
        caminho,
        {
            "config": config,
            "request": request,
        },
    )

@app.get("/PowerBi/{hub}")
async def powerbi_hubs(
    request: Request,
    hub: str,
):
    mapa_models = {
        "Arq": ("PowerBiArq", "./Arqueologia/PowerBi.html"),
        "Bio": ("PowerBiBio", "./Biodiversidade/PowerBi.html"),
        "Esp": ("PowerBiEsp", "./Espeleologia/PowerBi.html"),
        "Geo": ("PowerBiGeo", "./Geo/PowerBi.html"),
        "Hum": ("PowerBiHum", "./Humanidades/PowerBi.html"),
        "MF": ("PowerBiMF", "./MeioFisico/PowerBi.html"),
        "Mod": ("PowerBiMod", "./Modelagens/PowerBi.html"),
    }

    model, caminho = mapa_models.get(hub, (None, None))

    if not model or not caminho:
        return {"error": f"O hub '{hub}' não é válido."}

    return templates.TemplateResponse(
        caminho,
        {
            "config": config,
            "request": request,
        },
    )


#fim endpoints agenda
