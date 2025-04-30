from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ldap3 import Server, Connection, NTLM, ALL
from Crypto.Hash import MD4
from typing import Optional
from database.database import SessionLocal
from datetime import date, datetime
from starlette import status
from sidebar_config import SIDEBAR_MENUS
import hubs
import models
import hashlib

# Inicio Padroes FastAPI
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
config = {"ASSETS_ROOT": "/static/assets"}

hashlib.md4 = lambda: MD4.new()

LDAP_SERVER = "ldap://10.2.8.24"
LDAP_DOMAIN = "brandt.local"
LDAP_BASE_DN = "dc=brandt,dc=local"

# Fim Padroes FastAPI


# Banco inicio
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Banco FIm

# Inicio Funções


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
        "gabriel.rocha": "Arq",
        "vleite": "Arq",
        "rodrigo.pessoa": "Bio",
        "tlima": "Esp",
        "llacerda": "Geo",
        "agobira": "Hum",
        "vinicius.santos": "MeM",
        "clisboa": "MeM",
        "lthays": "Gerencia",
        "msantos": "Gerencia",
    }

    return user_routes.get(username.lower(), "Info")


async def get_Demandas(
    request: Request,
    hub: str,
    db: Session = Depends(get_db),
):
    model_class = hubs.get_model_demanda_by_hub(hub)
    if not model_class:
        raise HTTPException(status_code=400, detail=f"Hub '{hub}' não encontrado.")
    return db.query(model_class).all()


# Fim Funções

# inicio endpoints de login


@app.get("/")
async def login(request: Request):
    error_message = request.query_params.get("error")
    success_message = request.query_params.get("success")
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "config": config,
            "error_message": error_message,
            "success_message": success_message,
        },
    )


@app.post("/logar")
async def logar(username: str = Form(...), password: str = Form(...)):
    if authenticate_with_ad(username, password):
        redirect_url = get_redirect_url(username)
        return RedirectResponse(url=redirect_url, status_code=303)
    else:
        return RedirectResponse(url="/?error=Credenciais inválidas", status_code=303)


# fim endpoints de login

# inicio endpoints agenda


@app.get("/{hub}")
async def index_hubs(request: Request, hub: str):
    sidebar_items = SIDEBAR_MENUS.get(hub.upper())
    if not sidebar_items:
        raise HTTPException(
            status_code=400, detail="Hub inválido ou menus não encontrados."
        )

    return templates.TemplateResponse("index.html", {
        "request": request,
        "config": config,
        "hub_name": hub.upper(),
        "sidebar_items": sidebar_items
    })

@app.get("/PowerBi/{hub}")
async def powerbi_hubs(request: Request, hub: str):
    template = hubs.get_templates_by_hub(hub).get("powerbi")
    if not template:
        raise HTTPException(
            status_code=400, detail="Hub inválido ou template não encontrado."
        )
    return templates.TemplateResponse(template, {"request": request, "config": config})


@app.get("/Calendario/{hub}")
async def calendario_hubs(request: Request, hub: str):
    template = hubs.get_templates_by_hub(hub).get("calendario")
    if not template:
        raise HTTPException(
            status_code=400, detail="Hub inválido ou template não encontrado."
        )
    return templates.TemplateResponse(template, {"request": request, "config": config})


@app.get("/Agenda/{hub}")
async def agenda_hubs(
    request: Request,
    hub: str,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    model_class = hubs.get_model_demanda_by_hub(hub)
    template = hubs.get_templates_by_hub(hub).get("agenda")
    if not model_class or not template:
        raise HTTPException(status_code=400, detail="Hub inválido.")

    query = db.query(model_class)

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(model_class.dth_fim >= data_inicio_dt)
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(model_class.dth_inicio <= data_fim_dt)

    demandas = query.all()
    data = []
    for demanda in demandas:
        data.append(
            {
                "id": demanda.id,
                "titulo": demanda.titulo,
                "hub": demanda.hub,
                "responsavel": demanda.responsavel,
                "projeto": demanda.projeto,
                "atividade": demanda.atividade,
                "status": demanda.status,
                "dth_inicio": (
                    demanda.dth_inicio.strftime("%Y-%m-%d")
                    if demanda.dth_inicio
                    else None
                ),
                "dth_fim": (
                    demanda.dth_fim.strftime("%Y-%m-%d") if demanda.dth_fim else None
                ),
                "dtinicionp": (
                    demanda.dtinicionp.strftime("%Y-%m-%d")
                    if demanda.dtinicionp
                    else None
                ),
                "dtfimnp": (
                    demanda.dtfimnp.strftime("%Y-%m-%d") if demanda.dtfimnp else None
                ),
            }
        )


    sidebar_items = SIDEBAR_MENUS.get(hub.upper())
    if not sidebar_items:
        raise HTTPException(status_code=404, detail="Sidebar não encontrada para este hub.")

    hub_formatado = hub.lower()

    return templates.TemplateResponse("agenda.html", {
        "request": request,
        "config": config,
        "data": data,
        "hub_name": hubs.get_nome_legivel(hub),
        "sidebar_items": SIDEBAR_MENUS.get(hub.upper(), [])
    })



@app.get("/Netproject/{hub}")
async def netproject_hubs(
    request: Request,
    hub: str,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    model_class = hubs.get_model_hora_real_by_hub(hub)
    template = hubs.get_templates_by_hub(hub).get("netproject")
    if not model_class or not template:
        raise HTTPException(status_code=400, detail="Hub inválido.")

    try:
        data_inicio_dt = (
            datetime.strptime(data_inicio, "%Y-%m-%d") if data_inicio else None
        )
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d") if data_fim else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido.")

    query = db.query(model_class)
    if data_inicio_dt:
        query = query.filter(model_class.dth_inicio >= data_inicio_dt)
    if data_fim_dt:
        query = query.filter(model_class.dth_prevista <= data_fim_dt)

    demanda = query.all()
    for item in demanda:
        item.dth_inicio = (
            item.dth_inicio.strftime("%d-%m-%Y") if item.dth_inicio else None
        )
        item.dth_prevista = (
            item.dth_prevista.strftime("%d-%m-%Y") if item.dth_prevista else None
        )

    data_calendar = await get_Demandas(request=request, hub=hub, db=db)
    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar
    data = [
        item
        for item in demanda
        if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]

    return templates.TemplateResponse("netproject.html", {
        "request": request,
        "config": config,
        "hub_name": hubs.get_nome_legivel(hub),
        "sidebar_items": SIDEBAR_MENUS.get(hub.upper(), []),
        "data": data
    })


@app.get("/edit/{hub}/{id}")
async def edit_demanda(
    request: Request, hub: str, id: int, db: Session = Depends(get_db)
):
    model_class = hubs.get_model_hora_real_by_hub(hub)
    template = hubs.get_templates_by_hub(hub).get("edit_simples")
    if not model_class or not template:
        raise HTTPException(status_code=400, detail="Hub inválido.")

    projeto = db.query(model_class).filter(model_class.id == id).first()
    if not projeto:
        raise HTTPException(status_code=404, detail="Demanda não encontrada.")

    return templates.TemplateResponse(
        template, {"request": request, "demanda": projeto, "config": config}
    )


@app.post("/add/{hub}")
async def add_demanda(
    request: Request,
    hub: str,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    hub_banco: str = Form(...),
    db: Session = Depends(get_db),
):
    model_class = hubs.get_model_demanda_by_hub(hub)
    if not model_class:
        raise HTTPException(status_code=400, detail=f"Hub '{hub}' não é válido.")

    nova_demanda = model_class(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub_banco,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )

    db.add(nova_demanda)
    db.commit()

    return RedirectResponse(
        url=f"/Netproject/{hub}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/delete/{hub}/{id}")
async def delete_demanda(
    request: Request, hub: str, id: int, db: Session = Depends(get_db)
):
    model_class = hubs.get_model_demanda_by_hub(hub)
    if not model_class:
        raise HTTPException(status_code=400, detail=f"Hub '{hub}' não é válido.")

    demanda = db.query(model_class).filter(model_class.id == id).first()
    if not demanda:
        raise HTTPException(status_code=404, detail="Demanda não encontrada.")

    db.delete(demanda)
    db.commit()

    return RedirectResponse(url=f"/Agenda/{hub}", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit_agenda/{hub}/{id}")
async def edit_agenda(
    request: Request, hub: str, id: int, db: Session = Depends(get_db)
):
    model_demanda = hubs.get_model_demanda_by_hub(hub)
    model_hora = hubs.get_model_hora_real_by_hub(hub)
    template = hubs.get_templates_by_hub(hub).get("edit")

    if not model_demanda or not model_hora or not template:
        raise HTTPException(status_code=400, detail=f"Hub '{hub}' não é válido.")

    projeto = db.query(model_demanda).filter(model_demanda.id == id).first()
    if not projeto:
        raise HTTPException(status_code=404, detail="Demanda não encontrada.")

    netproject = (
        db.query(model_hora)
        .filter(
            model_hora.cod_projeto == projeto.cod_projeto,
            model_hora.nom_usuario == projeto.responsavel,
        )
        .first()
    )

    return templates.TemplateResponse(
        template,
        {
            "request": request,
            "demanda": projeto,
            "netproject": netproject,
            "config": config,
        },
    )


@app.post("/editAgenda/{hub}/{id}")
async def edit_agenda_post(
    hub: str,
    id: int,
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    hub_banco: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    model_class = hubs.get_model_demanda_by_hub(hub)
    if not model_class:
        raise HTTPException(status_code=400, detail=f"Hub '{hub}' não é válido.")

    demanda = db.query(model_class).filter(model_class.id == id).first()
    if not demanda:
        raise HTTPException(status_code=404, detail="Demanda não encontrada.")

    demanda.horas_np = horasNP
    demanda.status = status_projeto
    demanda.n_hora_hub = horas
    demanda.dth_fim = dth_fim
    demanda.dth_inicio = dth_inicio
    demanda.dtfimnp = dtfimnp
    demanda.hub = hub_banco
    demanda.titulo = titulo
    demanda.responsavel = responsavel
    demanda.projeto = projeto
    demanda.dtinicionp = dtinicionp
    demanda.atividade = atividade
    demanda.cod_projeto = cod_projeto

    db.commit()

    return RedirectResponse(url=f"/Agenda/{hub}", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/CadNaoProgramadas/{hub}")
async def cad_nao_programadas(request: Request, hub: str):
    template = hubs.get_templates_by_hub(hub).get("naoprogramadas")
    if not template:
        raise HTTPException(
            status_code=400, detail="Hub inválido ou template não encontrado."
        )
    return templates.TemplateResponse(template, {"request": request, "config": config})


@app.post("/addNaoProgramadas/{hub}")
async def add_nao_programadas(
    hub: str,
    request: Request,
    atividade: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    hub_banco: str = Form(...),
    db: Session = Depends(get_db),
):
    model_class = hubs.get_model_demanda_by_hub(hub)
    if not model_class:
        raise HTTPException(status_code=400, detail="Hub inválido.")

    demanda = model_class(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub_banco,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()

    return RedirectResponse(url=f"/Agenda/{hub}", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/Aquisicao/{hub}")
async def aquisicao(
    request: Request,
    hub: str,
    db: Session = Depends(get_db),
):
    model_name, template_path = hubs.mapa_aquisicao.get(hub, (None, None))

    if not model_name or not template_path:
        raise HTTPException(status_code=400, detail=f"Hub '{hub}' não é válido.")

    model_class = getattr(models, model_name, None)
    if not model_class:
        raise HTTPException(
            status_code=400, detail=f"Modelo '{model_name}' não encontrado."
        )

    dados = db.query(model_class).all()

    return templates.TemplateResponse(
        template_path, {"request": request, "config": config, "data": dados}
    )


# fim endpoints agenda
