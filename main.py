import unicodedata
from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
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

from hubs import mapa_models_demanda

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
        "gabriel.rocha": "Gerencia",
        "vleite": "Arq",
        "rodrigo.pessoa": "Bio",
        "tlima": "Esp",
        "llacerda": "Geo",
        "agobira": "Hum",
        "vinicius.santos": "MF",
        "clisboa": "Mod",
        "lthays": "Gerencia",
        "msantos": "Gerencia",
        "davi.santos": "Mod",
        "artur.cosenza": "Gerencia",
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


def remover_acentos(texto):
    return (
        unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    )


def limpar_gerencia(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFD", texto)
    texto_sem_acentos = "".join(
        c for c in texto_normalizado if unicodedata.category(c) != "Mn"
    )

    texto_limpo = texto_sem_acentos.lower().replace("gerencia", "").strip()

    return texto_limpo.title() 


# Fim Funções

# inicio endpoints de login

app.add_middleware(SessionMiddleware, secret_key="brandtmeioambiente@2025")

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
async def logar(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_with_ad(username, password):
        request.session["username"] = username
        redirect_url = get_redirect_url(username)
        return RedirectResponse(url=redirect_url, status_code=303)
    else:
        return RedirectResponse(url="/?error=Credenciais inválidas", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
# fim endpoints de login


# inicio endpoints agenda
# Gerencia inicio
@app.get("/Gerencia", response_class=HTMLResponse)
async def gerencia(request: Request):
    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)
    
    return templates.TemplateResponse("Gerencia/index.html", {"request": request})


# Gerencia fim


@app.get("/{hub}")
async def index_hubs(request: Request, hub: str):
    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)

    if hub.lower() == "info":
        return templates.TemplateResponse(
            "info.html",  # Seu template específico
            {
                "request": request,
                "config": config,
                "usuario": usuario,
            },
        )

    sidebar_items = hubs.get_sidebar_by_hub(hub)
    if not sidebar_items:
        raise HTTPException(
            status_code=400, detail="Hub inválido ou menus não encontrados."
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "config": config,
            "hub_name": hubs.get_nome_legivel(hub),
            "sidebar_items": sidebar_items,
        },
    )


@app.get("/PowerBi/{hub}")
async def powerbi_hubs(request: Request, hub: str):
    src_link = hubs.get_powerbi_link(hub)
    if not src_link:
        raise HTTPException(status_code=400, detail="Link do Power BI não encontrado.")
    sidebar_items = hubs.get_sidebar_by_hub(hub)
    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)
    
    return templates.TemplateResponse(
        "powerbi.html",
        {
            "request": request,
            "config": config,
            "hub_name": hubs.get_nome_legivel(hub),
            "sidebar_items": sidebar_items,
            "src": src_link,
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
    model_class = hubs.get_model_demanda_by_hub(hub)
    template = hubs.get_templates_by_hub(hub).get("agenda")
    if not model_class or not template:
        raise HTTPException(status_code=400, detail="Hub inválido.")

    query = db.query(model_class)
    if data_inicio:
        query = query.filter(
            model_class.dth_fim >= datetime.strptime(data_inicio, "%Y-%m-%d")
        )
    if data_fim:
        query = query.filter(
            model_class.dth_inicio <= datetime.strptime(data_fim, "%Y-%m-%d")
        )

    data = [
        {
            "id": d.id,
            "titulo": d.titulo,
            "hub": d.hub,
            "responsavel": d.responsavel,
            "projeto": d.projeto,
            "atividade": d.atividade,
            "status": d.status,
            "dth_inicio": d.dth_inicio.strftime("%d/%m/%Y") if d.dth_inicio else None,
            "dth_fim": d.dth_fim.strftime("%d/%m/%Y") if d.dth_fim else None,
            "dtinicionp": d.dtinicionp.strftime("%d/%m/%Y") if d.dtinicionp else None,
            "dtfimnp": d.dtfimnp.strftime("%d/%m/%Y") if d.dtfimnp else None,

        }
        for d in query.all()
    ]

    sidebar_items = hubs.get_sidebar_by_hub(hub)
    
    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)
    
    return templates.TemplateResponse(
        "agenda.html",
        {
            "request": request,
            "config": config,
            "data": data,
            "hub_name": hubs.get_nome_legivel(hub),
            "sidebar_items": sidebar_items,
            "hub_id": hub,
            "hub_name_banco": hubs.get_nome_legivel(hub).replace("GERENCIA", "").strip(),
        },
    )


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
    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)
    
    return templates.TemplateResponse(
        "netproject.html",
        {
            "request": request,
            "config": config,
            "hub_name": hubs.get_nome_legivel(hub),
            "sidebar_items": SIDEBAR_MENUS.get(hub.upper(), []),
            "data": data,
            "hub_id": hub,
        },
    )


@app.get("/edit/{hub}/{id}")
async def edit_demanda(
    request: Request, hub: str, id: int, db: Session = Depends(get_db)
):
    model_class = hubs.get_model_hora_real_by_hub(hub)
    template = "edit_simples.html"
    if not model_class:
        raise HTTPException(status_code=400, detail="Hub inválido.")

    projeto = db.query(model_class).filter(model_class.id == id).first()
    if not projeto:
        raise HTTPException(status_code=404, detail="Demanda não encontrada.")

    hub_name_sem_acentos = remover_acentos(hubs.get_nome_legivel(hub))
    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)
    
    return templates.TemplateResponse(
        template,
        {
            "request": request,
            "demanda": projeto,
            "config": config,
            "hub_name": hubs.get_nome_legivel(hub),
            "hub_id": hub,
            "sidebar_items": SIDEBAR_MENUS.get(hub.upper(), []),
            "hub_banco": hub_name_sem_acentos,
            "hub_banco_limpo": limpar_gerencia(hub_name_sem_acentos)
        },
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
    template = "edit_agenda.html"  # Um único template para todos os hubs

    if not model_demanda or not model_hora:
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

    hub_name_sem_acentos = remover_acentos(hubs.get_nome_legivel(hub))

    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)
    
    return templates.TemplateResponse(
        template,
        {
            "request": request,
            "demanda": projeto,
            "netproject": netproject,
            "config": config,
            "hub_id": hub,
            "hub_name": hubs.get_nome_legivel(hub),
            "sidebar_items": SIDEBAR_MENUS.get(hub.upper(), []),
            "hub_banco": hub_name_sem_acentos,
            "hub_banco_limpo": limpar_gerencia(hub_name_sem_acentos)
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
    sidebar_items = hubs.get_sidebar_by_hub(hub)
    hub_name = hubs.get_nome_legivel(hub)
    hub_name_sem_acentos = remover_acentos(hubs.get_nome_legivel(hub))
    colaboradores = hubs.get_colaboradores_por_hub(hub)
    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)
    
    return templates.TemplateResponse(
        "nao_programadas.html",
        {
            "request": request,
            "config": config,
            "hub_name": hub_name,
            "sidebar_items": sidebar_items,
            "hub_banco": hub_name_sem_acentos,
            "sidebar_items": SIDEBAR_MENUS.get(hub.upper(), []),
            "colaboradores": colaboradores,
            "hub_id": hub,
            "hub_banco_limpo": limpar_gerencia(hub_name_sem_acentos)
        },
    )


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
    model_name = hubs.mapa_aquisicao.get(hub, (None,))[
        0
    ] 

    if not model_name:
        raise HTTPException(status_code=400, detail=f"Hub '{hub}' não é válido.")

    model_class = getattr(models, model_name, None)
    if not model_class:
        raise HTTPException(
            status_code=400, detail=f"Modelo '{model_name}' não encontrado."
        )

    dados = db.query(model_class).all()
    usuario = request.session.get("username")
    if not usuario:
        return RedirectResponse(url="/?error=Não autenticado", status_code=303)
    
    return templates.TemplateResponse(
        "aquisicao.html",
        {
            "request": request,
            "config": config,
            "data": dados,
            "hub_name": hubs.get_nome_legivel(hub),
            "sidebar_items": SIDEBAR_MENUS.get(hub.upper(), []),
        },
    )

@app.get("/Calendario/{hub}/json")
async def calendario_json(hub: str, db: Session = Depends(get_db)):
    if hub not in mapa_models_demanda:
        raise HTTPException(status_code=404, detail=f"Hub '{hub}' não encontrado.")

    Model = mapa_models_demanda[hub]
    demandas = db.query(Model).all()

    eventos = []
    for demanda in demandas:
        evento = {
            "title": demanda.responsavel or "Sem responsável",
            "start": demanda.dth_inicio.isoformat() if demanda.dth_inicio else None,
            "end": demanda.dth_fim.isoformat() if demanda.dth_fim else None,
            "colaborador": demanda.responsavel or "",
            "projeto": demanda.projeto or "",
            "atividade": demanda.atividade or "",
            "hub": demanda.hub or "",
            "status": demanda.status or "",
        }
        eventos.append(evento)

    return eventos     


@app.get("/Calendario/{hub}")
async def calendario_hubs(request: Request, hub: str, db: Session = Depends(get_db)):
    # Buscar o template pelo hub
    template = hubs.get_templates_by_hub(hub).get("calendario")
    if not template:
        raise HTTPException(
            status_code=400, detail="Hub inválido ou template não encontrado."
        )

    # Verifica se o modelo de demanda existe para o hub
    modelo = mapa_models_demanda.get(hub)
    if not modelo:
        raise HTTPException(status_code=400, detail="Hub inválido (modelo não encontrado).")

    # Consulta as demandas do banco
    demandas = db.query(modelo).all()

    eventos = []
    for demanda in demandas:
        eventos.append({
            "title": demanda.titulo,                # Responsável pelo evento
            "start": demanda.dth_inicio.isoformat() if demanda.dth_inicio else None,
            "end": demanda.dth_fim.isoformat() if demanda.dth_fim else None,
            "colaborador": demanda.responsavel,
            "projeto": demanda.projeto,
            "atividade": demanda.atividade,
            "description": demanda.status               # Usando "status" como descrição
        })

    return templates.TemplateResponse(
        template,  {
            "request": request,
            "config": config,
            "evento": eventos,
            "hub":hub,
            "hub_name": hubs.get_nome_legivel(hub),
            "sidebar_items": SIDEBAR_MENUS.get(hub.upper(), []),
        },
    )


# fim endpoints agenda