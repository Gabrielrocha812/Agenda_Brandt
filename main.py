from fastapi import  Depends, FastAPI, Form, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from ldap3 import Server, Connection, NTLM, ALL
from Crypto.Hash import MD4
from typing import Optional
from database.database import SessionLocal
from datetime import date, datetime

import models
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

#Banco inicio
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Banco FIm

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
        "gabriel.rocha" : "Arq",
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

@app.get("/Calendario/{hub}")
async def calendario_hubs(
    request: Request,
    hub: str,
):
    mapa_models = {
        "Arq": ("CalendarioArq", "./Arqueologia/calendario.html"),
        "Bio": ("CalendarioBio", "./Biodiversidade/calendario.html"),
        "Esp": ("CalendarioEsp", "./Espeleologia/calendario.html"),
        "Geo": ("CalendarioGeo", "./Geo/calendario.html"),
        "Hum": ("CalendarioHum", "./Humanidades/calendario.html"),
        "MF": ("CalendarioMF", "./MeioFisico/calendario.html"),
        "Mod": ("CalendarioMod", "./Modelagens/calendario.html"),
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

@app.get("/Agenda/{hub}")
async def agenda_hubs(
    request: Request,
    hub: str,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    mapa_models = {
        "Arq": (models.Demandas_Arqueologia, "./Arqueologia/agenda.html"),
        "Bio": (models.Demandas_Biodiversidade, "./Biodiversidade/agenda.html"),
        "Esp": (models.Demandas_Espeleologia, "./Espeleologia/agenda.html"),
        "Geo": (models.Demandas_Geo, "./Geo/agenda.html"),
        "Hum": (models.Demandas_Humanidades, "./Humanidades/agenda.html"),
        "MF": (models.Demandas_MeioFisico, "./MeioFisico/agenda.html"),
        "Mod": (models.Demandas_Modelagens, "./Modelagens/agenda.html"),
    }

    model_class, caminho_template = mapa_models.get(hub, (None, None))

    if not model_class or not caminho_template:
        return {"error": f"O hub '{hub}' não é válido."}

    query = db.query(model_class).options(joinedload(model_class.hora_real_usuario))

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(model_class.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(model_class.dth_inicio <= data_fim_dt)

    demandas = query.all()

    data = []
    for demanda in demandas:
        horas_data = [
            {
                "pai": hora.pai,
                "total_horas_alocadas": hora.total_horas_alocadas,
                "nom_projeto": hora.nom_projeto,
                "nom_usuario": hora.nom_usuario,
                "dth_inicio": hora.dth_inicio.strftime("%d-%m-%Y") if hora.dth_inicio else None,
                "dth_prevista": hora.dth_prevista.strftime("%d-%m-%Y") if hora.dth_prevista else None,
            }
            for hora in demanda.hora_real_usuario
        ]

        data.append({
            "id": demanda.id,
            "titulo": demanda.titulo,
            "hub": demanda.hub,
            "responsavel": demanda.responsavel,
            "projeto": demanda.projeto,
            "atividade": demanda.atividade,
            "status": demanda.status,
            "dth_inicio": demanda.dth_inicio.strftime("%d-%m-%Y") if demanda.dth_inicio else None,
            "dth_fim": demanda.dth_fim.strftime("%d-%m-%Y") if demanda.dth_fim else None,
            "hora_real_usuario": horas_data,
        })

    return templates.TemplateResponse(
        caminho_template,
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

#fim endpoints agenda
