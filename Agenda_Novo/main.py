import logging
from fastapi import FastAPI, Request, Form, status, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.database import SessionLocal
from datetime import date, datetime
import models
from sqlalchemy.orm import joinedload

app = FastAPI()

# Defina o diretório para os arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        


templates = Jinja2Templates(directory="templates")
config = {"ASSETS_ROOT": "/static/assets"}
from typing import Optional
    
@app.get("/", response_class=HTMLResponse)
async def login(
    request: Request
):
    return templates.TemplateResponse("./login.html", {"request": request})

async def get_Demandas(
    request: Request, 
    db: Session = Depends(get_db), 
):
    demanda = db.query(models.Demandas_Geo).all()

    return demanda

async def get_Demandas_Arq(
    request: Request, 
    db: Session = Depends(get_db), 
):
    demanda = db.query(models.Demandas_Arqueologia).all()

    return demanda

async def get_Demandas_Bio(
    request: Request, 
    db: Session = Depends(get_db), 
):
    demanda = db.query(models.Demandas_Biodiversidade).all()

    return demanda

async def get_Demandas_Esp(
    request: Request, 
    db: Session = Depends(get_db), 
):
    demanda = db.query(models.Demandas_Espeleologia).all()

    return demanda

async def get_Demandas_Hum(
    request: Request, 
    db: Session = Depends(get_db), 
):
    demanda = db.query(models.Demandas_Humanidades).all()

    return demanda

async def get_Demandas_MF(
    request: Request, 
    db: Session = Depends(get_db), 
):
    demanda = db.query(models.Demandas_MeioFisico).all()

    return demanda

async def get_Demandas_Mod(
    request: Request, 
    db: Session = Depends(get_db), 
):
    demanda = db.query(models.Demandas_Modelagens).all()

    return demanda

async def get_Demandas_Gestao(
    request: Request, 
    db: Session = Depends(get_db), 
):
    demanda = db.query(models.Demandas_Gestao).all()

    return demanda

#inicio arqueologia
@app.post("/addArq")
async def addArq(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas_Arqueologia(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("arqnetproject"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadArqNaoProgramadas", response_class=HTMLResponse)
async def CadArqNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Arqueologia/naoprogramadas.html", {"request": request, "config": config})


@app.post("/addNaoProgramadasArq")
async def addNaoProgramadasArq(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas_Arqueologia(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_arq"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.post("/editArqAgenda/{id}")
async def editArq_agenda(
    id: int,
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas_Arqueologia).filter(models.Demandas_Arqueologia.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_arq"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/Arq", response_class=HTMLResponse)
async def inicio_arq(
    request: Request
):
    return templates.TemplateResponse("./Arqueologia/index.html", {"request": request})

@app.get("/PowerBiArq", response_class=HTMLResponse)
async def powerbi_arq(
    request: Request
):
    return templates.TemplateResponse("./Arqueologia/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioArq", response_class=HTMLResponse)
async def calendario_Arq(request: Request):
    return templates.TemplateResponse("Arqueologia/calendario.html", {"request": request, "config": config})

@app.get("/ArqAgenda")
async def agenda_arq(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    
    query = (
        db.query(models.Demandas_Arqueologia)
        .options(joinedload(models.Demandas_Arqueologia.hora_real_usuario))  
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Arqueologia.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Arqueologia.dth_inicio <= data_fim_dt)

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
        "./Arqueologia/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/ArqNetproject")
async def arqnetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    # Logando os parâmetros recebidos
    logging.info(f"Parâmetros recebidos - data_inicio: {data_inicio}, data_fim: {data_fim}")
    
    # Converta as strings de data em objetos datetime
    data_inicio_dt = None
    data_fim_dt = None
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            logging.info(f"data_inicio convertido: {data_inicio_dt}")
        except ValueError as e:
            logging.error(f"Erro ao converter data_inicio: {e}")
            
    if data_fim:
        try:
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
            logging.info(f"data_fim convertido: {data_fim_dt}")
        except ValueError as e:
            logging.error(f"Erro ao converter data_fim: {e}")
    
    # Realize a consulta ao banco de dados
    query = db.query(models.hora_real_arqueologia)
    
    # Filtros de data
    if data_inicio_dt and data_fim_dt:
        query = query.filter(
            models.hora_real_arqueologia.dth_inicio >= data_inicio_dt,
            models.hora_real_arqueologia.dth_prevista <= data_fim_dt
        )
    elif data_inicio_dt:
        query = query.filter(models.hora_real_arqueologia.dth_inicio >= data_inicio_dt)
    elif data_fim_dt:
        query = query.filter(models.hora_real_arqueologia.dth_prevista <= data_fim_dt)
    
    demanda = query.all()

    # Logando a quantidade de resultados encontrados
    logging.info(f"Quantidade de resultados encontrados: {len(demanda)}")

    # Formatando as datas
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    # Comparação adicional, se necessário
    data_calendar = await get_Demandas_Arq(request=request, db=db)
    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]


    return templates.TemplateResponse(
        "./Arqueologia/netproject.html",
        {
            "config": config,
            "request": request,
            "data": list(data),
        },
    )

@app.get("/editarq/{id}")
async def edit_arq(request: Request, id: int, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_arqueologia)
        .filter(models.hora_real_arqueologia.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "/Arqueologia/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_arq_agenda/{id}")
async def edit_arq_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    # Consulta na tabela Demandas para pegar o cod_projeto e nom_usuario
    projeto = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    if projeto:
        cod_projeto1 = projeto.cod_projeto  # Atribuindo o valor de cod_projeto
        nom_usuario1 = projeto.responsavel  # Atribuindo o valor de nom_usuario
    else:
        cod_projeto1 = None  # Caso não encontre o projeto, define como None
        nom_usuario1 = None  # Caso não encontre o projeto, define como None
    
    # Verificando os valores atribuídos
    print(f"Valor de cod_projeto1: {cod_projeto1}")
    print(f"Valor de nom_usuario1: {nom_usuario1}")

    # Consulta na tabela hora_real_usuario utilizando os valores dinâmicos de cod_projeto1 e nom_usuario1
    netproject = (
        db.query(models.hora_real_arqueologia)
        .filter(
            models.hora_real_arqueologia.cod_projeto == cod_projeto1,  # Filtro para cod_projeto
            models.hora_real_arqueologia.nom_usuario == nom_usuario1   # Filtro para nom_usuario
        )
        .first()
    )

    # Verificando o resultado da consulta
    print(f'netproject: {netproject}')
    
    return templates.TemplateResponse(
        "/Arqueologia/edit_agenda.html", {"request": request, "demanda": projeto, "netproject": netproject, "config": config}
    )

@app.get("/delete_arq_agenda/{id}")
async def delete_arq(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_geo = db.query(models.Demandas_Arqueologia).filter(models.Demandas_Arqueologia.id == id).first()
    db.delete(demanda_agenda_geo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_arq"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarArq")
async def get_calendararq(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Arqueologia)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data

#fim arqueologia

  
#inicio geo

@app.post("/addGeo")
async def addGeo(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_geo"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadGeoNaoProgramadas", response_class=HTMLResponse)
async def CadGeoNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Geo/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasGeo")
async def addNaoProgramadasGeo(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_geo"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.post("/editGeoAgenda/{id}")
async def editGeo_agenda(
    id: int,
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    
    demanda.horas_np = horasNP
    demanda.status = status_projeto
    demanda.n_hora_hub = horas
    demanda.dth_fim = dth_fim
    demanda.dth_inicio = dth_inicio
    demanda.dtfimnp = dtfimnp
    demanda.hub = hub
    demanda.titulo = titulo
    demanda.responsavel = responsavel
    demanda.projeto = projeto
    demanda.dtinicionp = dtinicionp
    demanda.atividade = atividade
    demanda.cod_projeto = cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_geo"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/Geo", response_class=HTMLResponse)
async def inicio_geo(
    request: Request
):
    return templates.TemplateResponse("./Geo/index.html", {"request": request})

@app.get("/PowerBi", response_class=HTMLResponse)
async def powerbi_geo(
    request: Request
):
    return templates.TemplateResponse("./Geo/powerbi.html", {"request": request, "config": config})

@app.get("/Calendario", response_class=HTMLResponse)
async def calendario_geo(request: Request):
    return templates.TemplateResponse("Geo/calendario.html", {"request": request, "config": config})

@app.get("/GeoAgenda")
async def agenda_geo(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Geo)
        .options(joinedload(models.Demandas_Geo.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Geo.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Geo.dth_inicio <= data_fim_dt)

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
        "./Geo/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/GeoNetproject")
async def geonetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    # Logando os parâmetros recebidos
    logging.info(f"Parâmetros recebidos - data_inicio: {data_inicio}, data_fim: {data_fim}")
    
    # Converta as strings de data em objetos datetime
    data_inicio_dt = None
    data_fim_dt = None
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            logging.info(f"data_inicio convertido: {data_inicio_dt}")
        except ValueError as e:
            logging.error(f"Erro ao converter data_inicio: {e}")
            
    if data_fim:
        try:
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
            logging.info(f"data_fim convertido: {data_fim_dt}")
        except ValueError as e:
            logging.error(f"Erro ao converter data_fim: {e}")
    
    # Realize a consulta ao banco de dados
    query = db.query(models.hora_real_geo)
    
    # Filtros de data
    if data_inicio_dt and data_fim_dt:
        query = query.filter(
            models.hora_real_geo.dth_inicio >= data_inicio_dt,
            models.hora_real_geo.dth_prevista <= data_fim_dt
        )
    elif data_inicio_dt:
        query = query.filter(models.hora_real_geo.dth_inicio >= data_inicio_dt)
    elif data_fim_dt:
        query = query.filter(models.hora_real_geo.dth_prevista <= data_fim_dt)
    
    demanda = query.all()

    # Logando a quantidade de resultados encontrados
    logging.info(f"Quantidade de resultados encontrados: {len(demanda)}")

    # Formatando as datas
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    # Comparação adicional, se necessário
    data_calendar = await get_Demandas(request=request, db=db)
    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]


    return templates.TemplateResponse(
        "./Geo/netproject.html",
        {
            "config": config,
            "request": request,
            "data": list(data),
        },
    )

@app.get("/edit_geo/{id}")
async def edit_geo(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_usuario)
        .filter(models.hora_real_usuario.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "/Geo/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_geo_agenda/{id}")
async def edit_geo_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    # Consulta na tabela Demandas para pegar o cod_projeto e nom_usuario
    projeto = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    if projeto:
        cod_projeto1 = projeto.cod_projeto  # Atribuindo o valor de cod_projeto
        nom_usuario1 = projeto.responsavel  # Atribuindo o valor de nom_usuario
    else:
        cod_projeto1 = None  # Caso não encontre o projeto, define como None
        nom_usuario1 = None  # Caso não encontre o projeto, define como None
    
    # Verificando os valores atribuídos
    print(f"Valor de cod_projeto1: {cod_projeto1}")
    print(f"Valor de nom_usuario1: {nom_usuario1}")

    # Consulta na tabela hora_real_usuario utilizando os valores dinâmicos de cod_projeto1 e nom_usuario1
    netproject = (
        db.query(models.hora_real_usuario)
        .filter(
            models.hora_real_usuario.cod_projeto == cod_projeto1,  # Filtro para cod_projeto
            models.hora_real_usuario.nom_usuario == nom_usuario1   # Filtro para nom_usuario
        )
        .first()
    )

    # Verificando o resultado da consulta
    print(f'netproject: {netproject}')
    
    return templates.TemplateResponse(
        "/Geo/edit_agenda.html", {"request": request, "demanda": projeto, "netproject": netproject, "config": config}
    )

@app.get("/delete_geo_agenda/{id}")
async def delete_geo(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_geo = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_geo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_geo"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarGeo")
async def get_calendargeo(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Geo)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim geo


#inicio bio

@app.post("/addBio")
async def addBio(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_bio"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadBioNaoProgramadas", response_class=HTMLResponse)
async def CadBioNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Biodiversidade/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasBio")
async def addNaoProgramadasBio(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_bio"), status_code=status.HTTP_303_SEE_OTHER
    )
        
@app.post("/editBioAgenda/{id}")
async def editBio_agenda(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp:  Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp:  Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_bio"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/Bio", response_class=HTMLResponse)
async def inicio_bio(
    request: Request
):
    return templates.TemplateResponse("./Biodiversidade/index.html", {"request": request})

@app.get("/PowerBiBio", response_class=HTMLResponse)
async def powerbi_bio(
    request: Request
):
    return templates.TemplateResponse("./Biodiversidade/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioBio", response_class=HTMLResponse)
async def calendario_bio(request: Request):
    return templates.TemplateResponse("Biodiversidade/calendario.html", {"request": request, "config": config})

@app.get("/BioAgenda")
async def agenda_bio(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Biodiversidade)
        .options(joinedload(models.Demandas_Biodiversidade.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Biodiversidade.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Biodiversidade.dth_inicio <= data_fim_dt)

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
        "./Biodiversidade/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/BioNetproject")
async def bionetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    # Logando os parâmetros recebidos
    logging.info(f"Parâmetros recebidos - data_inicio: {data_inicio}, data_fim: {data_fim}")
    
    # Converta as strings de data em objetos datetime
    data_inicio_dt = None
    data_fim_dt = None
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            logging.info(f"data_inicio convertido: {data_inicio_dt}")
        except ValueError as e:
            logging.error(f"Erro ao converter data_inicio: {e}")
            
    if data_fim:
        try:
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
            logging.info(f"data_fim convertido: {data_fim_dt}")
        except ValueError as e:
            logging.error(f"Erro ao converter data_fim: {e}")
    
    # Realize a consulta ao banco de dados
    query = db.query(models.hora_real_biodiversidade)
    
    # Filtros de data
    if data_inicio_dt and data_fim_dt:
        query = query.filter(
            models.hora_real_biodiversidade.dth_inicio >= data_inicio_dt,
            models.hora_real_biodiversidade.dth_prevista <= data_fim_dt
        )
    elif data_inicio_dt:
        query = query.filter(models.hora_real_biodiversidade.dth_inicio >= data_inicio_dt)
    elif data_fim_dt:
        query = query.filter(models.hora_real_biodiversidade.dth_prevista <= data_fim_dt)
    
    demanda = query.all()

    # Logando a quantidade de resultados encontrados
    logging.info(f"Quantidade de resultados encontrados: {len(demanda)}")

    # Formatando as datas
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    # Comparação adicional, se necessário
    data_calendar = await get_Demandas_Bio(request=request, db=db)
    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]


    return templates.TemplateResponse(
        "./Biodiversidade/netproject.html",
        {
            "config": config,
            "request": request,
            "data": list(data),
        },
    )

@app.get("/edit_bio/{id}")
async def edit_bio(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_biodiversidade)
        .filter(models.hora_real_biodiversidade.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "/Biodiversidade/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_bio_agenda/{id}")
async def edit_bio_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    # Consulta na tabela Demandas para pegar o cod_projeto e nom_usuario
    projeto = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    if projeto:
        cod_projeto1 = projeto.cod_projeto  # Atribuindo o valor de cod_projeto
        nom_usuario1 = projeto.responsavel  # Atribuindo o valor de nom_usuario
    else:
        cod_projeto1 = None  # Caso não encontre o projeto, define como None
        nom_usuario1 = None  # Caso não encontre o projeto, define como None
    
    # Verificando os valores atribuídos
    print(f"Valor de cod_projeto1: {cod_projeto1}")
    print(f"Valor de nom_usuario1: {nom_usuario1}")

    # Consulta na tabela hora_real_usuario utilizando os valores dinâmicos de cod_projeto1 e nom_usuario1
    netproject = (
        db.query(models.hora_real_biodiversidade)
        .filter(
            models.hora_real_biodiversidade.cod_projeto == cod_projeto1,  # Filtro para cod_projeto
            models.hora_real_biodiversidade.nom_usuario == nom_usuario1   # Filtro para nom_usuario
        )
        .first()
    )

    # Verificando o resultado da consulta
    print(f'netproject: {netproject}')
    
    return templates.TemplateResponse(
        "/Biodiversidade/edit_agenda.html", {"request": request, "demanda": projeto, "netproject": netproject, "config": config}
    )

@app.get("/delete_bio_agenda/{id}")
async def delete_bio(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_bio = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_bio)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_bio"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarBio")
async def get_calendarbio(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Biodiversidade)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim bio


#inicio espeleologia

@app.post("/addEsp")
async def addEsp(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_esp"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadEspNaoProgramadas", response_class=HTMLResponse)
async def CadEspNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Espeleologia/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasEsp")
async def addNaoProgramadasEsp(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_esp"), status_code=status.HTTP_303_SEE_OTHER
    )
      
@app.post("/editEspAgenda/{id}")
async def editEsp_agenda(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp:  Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp:  Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_esp"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/Esp", response_class=HTMLResponse)
async def inicio_esp(
    request: Request
):
    return templates.TemplateResponse("./Espeleologia/index.html", {"request": request})

@app.get("/PowerBiEsp", response_class=HTMLResponse)
async def powerbi_esp(
    request: Request
):
    return templates.TemplateResponse("./Espeleologia/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioEsp", response_class=HTMLResponse)
async def calendario_esp(request: Request):
    return templates.TemplateResponse("Espeleologia/calendario.html", {"request": request, "config": config})

@app.get("/EspAgenda")
async def agenda_esp(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Espeleologia)
        .options(joinedload(models.Demandas_Espeleologia.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Espeleologia.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Espeleologia.dth_inicio <= data_fim_dt)

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
        "./Espeleologia/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/EspNetproject")
async def espnetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_Esp(request=request, db=db)
    
    query = db.query(models.hora_real_espeleologia)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_espeleologia.dth_inicio >= data_inicio_dt,
                models.hora_real_espeleologia.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_espeleologia.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_espeleologia.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Espeleologia/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_esp/{id}")
async def edit_esp(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_espeleologia)
        .filter(models.hora_real_espeleologia.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "/Espeleologia/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_esp_agenda/{id}")
async def edit_esp_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    # Consulta na tabela Demandas para pegar o cod_projeto e nom_usuario
    projeto = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    if projeto:
        cod_projeto1 = projeto.cod_projeto  # Atribuindo o valor de cod_projeto
        nom_usuario1 = projeto.responsavel  # Atribuindo o valor de nom_usuario
    else:
        cod_projeto1 = None  # Caso não encontre o projeto, define como None
        nom_usuario1 = None  # Caso não encontre o projeto, define como None
    
    # Verificando os valores atribuídos
    print(f"Valor de cod_projeto1: {cod_projeto1}")
    print(f"Valor de nom_usuario1: {nom_usuario1}")

    # Consulta na tabela hora_real_usuario utilizando os valores dinâmicos de cod_projeto1 e nom_usuario1
    netproject = (
        db.query(models.hora_real_espeleologia)
        .filter(
            models.hora_real_espeleologia.cod_projeto == cod_projeto1,  # Filtro para cod_projeto
            models.hora_real_espeleologia.nom_usuario == nom_usuario1   # Filtro para nom_usuario
        )
        .first()
    )

    # Verificando o resultado da consulta
    print(f'netproject: {netproject}')
    
    return templates.TemplateResponse(
        "/Espeleologia/edit_agenda.html", {"request": request, "demanda": projeto, "netproject": netproject, "config": config}
    )

@app.get("/delete_esp_agenda/{id}")
async def delete_esp(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_esp = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_esp)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_esp"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarEsp")
async def get_calendaresp(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Espeleologia)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim espeleologia

#inicio humanidades

@app.post("/addHum")
async def addHum(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("HumNetproject"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadHumNaoProgramadas", response_class=HTMLResponse)
async def CadHumNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Humanidades/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasHum")
async def addNaoProgramadasHum(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_hum"), status_code=status.HTTP_303_SEE_OTHER
    )
     
@app.post("/editHumAgenda/{id}")
async def editHum_agenda(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp:  Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_hum"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/Hum", response_class=HTMLResponse)
async def inicio_hum(
    request: Request
):
    return templates.TemplateResponse("./Humanidades/index.html", {"request": request})

@app.get("/PowerBiHum", response_class=HTMLResponse)
async def powerbi_hum(
    request: Request
):
    return templates.TemplateResponse("./Humanidades/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioHum", response_class=HTMLResponse)
async def calendario_hum(request: Request):
    return templates.TemplateResponse("Humanidades/calendario.html", {"request": request, "config": config})

@app.get("/HumAgenda")
async def agenda_hum(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Humanidades)
        .options(joinedload(models.Demandas_Humanidades.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Humanidades.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Humanidades.dth_inicio <= data_fim_dt)

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
        "./Humanidades/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/HumNetproject")
async def HumNetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_Hum(request=request, db=db)
    
    query = db.query(models.hora_real_humanidades)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_humanidades.dth_inicio >= data_inicio_dt,
                models.hora_real_humanidades.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_humanidades.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_humanidades.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Humanidades/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_hum/{id}")
async def edit_hum(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_humanidades)
        .filter(models.hora_real_humanidades.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "/Humanidades/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_hum_agenda/{id}")
async def edit_hum_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    # Consulta na tabela Demandas para pegar o cod_projeto e nom_usuario
    projeto = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    if projeto:
        cod_projeto1 = projeto.cod_projeto  # Atribuindo o valor de cod_projeto
        nom_usuario1 = projeto.responsavel  # Atribuindo o valor de nom_usuario
    else:
        cod_projeto1 = None  # Caso não encontre o projeto, define como None
        nom_usuario1 = None  # Caso não encontre o projeto, define como None
    
    # Verificando os valores atribuídos
    print(f"Valor de cod_projeto1: {cod_projeto1}")
    print(f"Valor de nom_usuario1: {nom_usuario1}")

    # Consulta na tabela hora_real_usuario utilizando os valores dinâmicos de cod_projeto1 e nom_usuario1
    netproject = (
        db.query(models.hora_real_humanidades)
        .filter(
            models.hora_real_humanidades.cod_projeto == cod_projeto1,  # Filtro para cod_projeto
            models.hora_real_humanidades.nom_usuario == nom_usuario1   # Filtro para nom_usuario
        )
        .first()
    )

    # Verificando o resultado da consulta
    print(f'netproject: {netproject}')
    
    return templates.TemplateResponse(
        "/Humanidades/edit_agenda.html", {"request": request, "demanda": projeto, "netproject": netproject, "config": config}
    )

@app.get("/delete_hum_agenda/{id}")
async def delete_hum(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_hum = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_hum)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_hum"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarHum")
async def get_calendarhum(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Humanidades)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim humanidades


#inicio MeioFisico

@app.post("/addMF")
async def addMF(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_mf"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadMFNaoProgramadas", response_class=HTMLResponse)
async def CadMFNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./MeioFisico/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasMF")
async def addNaoProgramadasMF(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_mf"), status_code=status.HTTP_303_SEE_OTHER
    )
             
@app.post("/editMFAgenda/{id}")
async def editMF_agenda(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_mf"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/MF", response_class=HTMLResponse)
async def inicio_mf(
    request: Request
):
    return templates.TemplateResponse("./MeioFisico/index.html", {"request": request})

@app.get("/PowerBiMF", response_class=HTMLResponse)
async def powerbi_mf(
    request: Request
):
    return templates.TemplateResponse("./MeioFisico/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioMF", response_class=HTMLResponse)
async def calendario_mf(request: Request):
    return templates.TemplateResponse("MeioFisico/calendario.html", {"request": request, "config": config})

@app.get("/MFAgenda")
async def agenda_mf(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_MeioFisico)
        .options(joinedload(models.Demandas_MeioFisico.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_MeioFisico.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_MeioFisico.dth_inicio <= data_fim_dt)

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
        "./MeioFisico/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/MFNetproject")
async def mfnetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_MF(request=request, db=db)
    
    query = db.query(models.hora_real_mfisico)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_mfisico.dth_inicio >= data_inicio_dt,
                models.hora_real_mfisico.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_mfisico.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_mfisico.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./MeioFisico/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_mf/{id}")
async def edit_mf(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_mfisico)
        .filter(models.hora_real_mfisico.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "/MeioFisico/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_mf_agenda/{id}")
async def edit_mf_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    # Consulta na tabela Demandas para pegar o cod_projeto e nom_usuario
    projeto = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    if projeto:
        cod_projeto1 = projeto.cod_projeto  # Atribuindo o valor de cod_projeto
        nom_usuario1 = projeto.responsavel  # Atribuindo o valor de nom_usuario
    else:
        cod_projeto1 = None  # Caso não encontre o projeto, define como None
        nom_usuario1 = None  # Caso não encontre o projeto, define como None
    
    # Verificando os valores atribuídos
    print(f"Valor de cod_projeto1: {cod_projeto1}")
    print(f"Valor de nom_usuario1: {nom_usuario1}")

    # Consulta na tabela hora_real_usuario utilizando os valores dinâmicos de cod_projeto1 e nom_usuario1
    netproject = (
        db.query(models.hora_real_mfisico)
        .filter(
            models.hora_real_mfisico.cod_projeto == cod_projeto1,  # Filtro para cod_projeto
            models.hora_real_mfisico.nom_usuario == nom_usuario1   # Filtro para nom_usuario
        )
        .first()
    )

    # Verificando o resultado da consulta
    print(f'netproject: {netproject}')
    
    return templates.TemplateResponse(
        "/MeioFisico/edit_agenda.html", {"request": request, "demanda": projeto, "netproject": netproject, "config": config}
    )

@app.get("/delete_mf_agenda/{id}")
async def delete_mf(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_mf = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_mf)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_mf"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarMF")
async def get_calendarmf(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_MeioFisico)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim MeioFisico

#inicio Modelagens

@app.post("/addMod")
async def addMod(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return templates.TemplateResponse(
        "./Modelagens/agenda.html",
        {
            "config": config,
            "request": request,
        },
    )

@app.get("/CadModNaoProgramadas", response_class=HTMLResponse)
async def CadModNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Modelagens/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasMod")
async def addNaoProgramadasMod(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_mod"), status_code=status.HTTP_303_SEE_OTHER)
         
@app.post("/editModAgenda/{id}")
async def editMod_agenda(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return templates.TemplateResponse(
        "./Modelagens/agenda.html",
        {
            "config": config,
            "request": request,
        },
    )

@app.get("/Mod", response_class=HTMLResponse)
async def inicio_mod(
    request: Request
):
    return templates.TemplateResponse("./Modelagens/index.html", {"request": request})

@app.get("/PowerBiMod", response_class=HTMLResponse)
async def powerbi_mod(
    request: Request
):
    return templates.TemplateResponse("./Modelagens/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioMod", response_class=HTMLResponse)
async def calendario_mod(request: Request):
    return templates.TemplateResponse("Modelagens/calendario.html", {"request": request, "config": config})

@app.get("/ModAgenda")
async def agenda_mod(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Modelagens)
        .options(joinedload(models.Demandas_Modelagens.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Modelagens.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Modelagens.dth_inicio <= data_fim_dt)

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
        "./Modelagens/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/ModNetproject")
async def modnetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_Mod(request=request, db=db)
    
    query = db.query(models.hora_real_mmodelagens)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_mmodelagens.dth_inicio >= data_inicio_dt,
                models.hora_real_mmodelagens.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_mmodelagens.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_mmodelagens.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Modelagens/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_mod/{id}")
async def edit_mod(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_mmodelagens)
        .filter(models.hora_real_mmodelagens.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "/Modelagens/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_mod_agenda/{id}")
async def edit_mod_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    # Consulta na tabela Demandas para pegar o cod_projeto e nom_usuario
    projeto = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    if projeto:
        cod_projeto1 = projeto.cod_projeto  # Atribuindo o valor de cod_projeto
        nom_usuario1 = projeto.responsavel  # Atribuindo o valor de nom_usuario
    else:
        cod_projeto1 = None  # Caso não encontre o projeto, define como None
        nom_usuario1 = None  # Caso não encontre o projeto, define como None
    
    # Verificando os valores atribuídos
    print(f"Valor de cod_projeto1: {cod_projeto1}")
    print(f"Valor de nom_usuario1: {nom_usuario1}")

    # Consulta na tabela hora_real_usuario utilizando os valores dinâmicos de cod_projeto1 e nom_usuario1
    netproject = (
        db.query(models.hora_real_mmodelagens)
        .filter(
            models.hora_real_mmodelagens.cod_projeto == cod_projeto1,  # Filtro para cod_projeto
            models.hora_real_mmodelagens.nom_usuario == nom_usuario1   # Filtro para nom_usuario
        )
        .first()
    )

    # Verificando o resultado da consulta
    print(f'netproject: {netproject}')
    
    return templates.TemplateResponse(
        "/Modelagens/edit_agenda.html", {"request": request, "demanda": projeto, "netproject": netproject, "config": config}
    )

@app.get("/delete_mod_agenda/{id}")
async def delete_mod(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_mod = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_mod)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_mod"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/CalendarMod")
async def get_calendarmod(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Modelagens)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim Modelagens


#inicio admin
@app.get("/Gerencia")
async def gerencia(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/index.html", {"request": request, "config": config})

#inicio arqueologia
@app.post("/addArqGe")
async def addArqGe(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("arqnetprojectGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadArqNaoProgramadasGe", response_class=HTMLResponse)
async def CadArqNaoProgramadasGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Arqueologia/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasArqGe")
async def addNaoProgramadasArqGe(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_arqGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.post("/editArqAgendaGe/{id}")
async def editArq_agendaGe(
    id: int,
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_arqGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/ArqGe", response_class=HTMLResponse)
async def inicio_arqGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Arqueologia/index.html", {"request": request})

@app.get("/PowerBiArqGe", response_class=HTMLResponse)
async def powerbi_arqGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Arqueologia/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioArqGe", response_class=HTMLResponse)
async def calendario_ArqGe(request: Request):
    return templates.TemplateResponse("/Gerencia/Arqueologia/calendario.html", {"request": request, "config": config})

@app.get("/ArqAgendaGe")
async def agenda_arqGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    
    query = (
        db.query(models.Demandas_Arqueologia)
        .options(joinedload(models.Demandas_Arqueologia.hora_real_usuario))  
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Arqueologia.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Arqueologia.dth_inicio <= data_fim_dt)

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
        "./Gerencia/Arqueologia/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/ArqNetprojectGe")
async def arqnetprojectGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_Arq(request=request, db=db)
    
    query = db.query(models.hora_real_arqueologia)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_arqueologia.dth_inicio >= data_inicio_dt,
                models.hora_real_arqueologia.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_arqueologia.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_arqueologia.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Gerencia/Arqueologia/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/editarqGe/{id}")
async def edit_arqGe(request: Request, id: int, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_arqueologia)
        .filter(models.hora_real_arqueologia.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Arqueologia/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_arq_agendaGe/{id}")
async def edit_arq_agendaGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.Demandas)
        .filter(models.Demandas.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Arqueologia/edit_agenda.html", {"request": request, "demanda": projeto, "config": config}
    )

@app.get("/delete_arq_agendaGe/{id}")
async def delete_arqGe(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_geo = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_geo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_arqGe"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarArqGe")
async def get_calendararqGe(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Arqueologia)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data

#fim arqueologia

#inicio geo

@app.post("/addGeoGe")
async def addGeoGe(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_geoGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadGeoNaoProgramadasGe", response_class=HTMLResponse)
async def CadGeoNaoProgramadasGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Geo/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasGeoGe")
async def addNaoProgramadasGeoGe(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_geoGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.post("/editGeoAgendaGe/{id}")
async def editGeo_agendaGe(
    id: int,
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    
    demanda.horas_np = horasNP
    demanda.status = status_projeto
    demanda.n_hora_hub = horas
    demanda.dth_fim = dth_fim
    demanda.dth_inicio = dth_inicio
    demanda.dtfimnp = dtfimnp
    demanda.hub = hub
    demanda.titulo = titulo
    demanda.responsavel = responsavel
    demanda.projeto = projeto
    demanda.dtinicionp = dtinicionp
    demanda.atividade = atividade
    demanda.cod_projeto = cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_geoGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/GeoGe", response_class=HTMLResponse)
async def inicio_geoGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Geo/index.html", {"request": request})

@app.get("/PowerBiGe", response_class=HTMLResponse)
async def powerbi_geoGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Geo/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioGe", response_class=HTMLResponse)
async def calendario_geoGe(request: Request):
    return templates.TemplateResponse("./Gerencia/Geo/calendario.html", {"request": request, "config": config})

@app.get("/GeoAgendaGe")
async def agenda_geoGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Geo)
        .options(joinedload(models.Demandas_Geo.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Geo.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Geo.dth_inicio <= data_fim_dt)

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
        "./Gerencia/Geo/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/GeoNetprojectGe")
async def geonetprojectGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas(request=request, db=db)
    
    query = db.query(models.hora_real_geo)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_geo.dth_inicio >= data_inicio_dt,
                models.hora_real_geo.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_geo.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_geo.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Gerencia/Geo/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_geoGe/{id}")
async def edit_geoGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_usuario)
        .filter(models.hora_real_usuario.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Geo/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_geo_agendaGe/{id}")
async def edit_geo_agendaGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.Demandas)
        .filter(models.Demandas.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Geo/edit_agenda.html", {"request": request, "demanda": projeto, "config": config}
    )

@app.get("/delete_geo_agendaGe/{id}")
async def delete_geoGe(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_geo = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_geo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_geoGe"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarGeoGe")
async def get_calendargeoGe(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Geo)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim geo

#inicio espeleologia

@app.post("/addEspGe")
async def addEspGe(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_espGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadEspNaoProgramadasGe", response_class=HTMLResponse)
async def CadEspNaoProgramadasGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Espeleologia/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasEspGe")
async def addNaoProgramadasEspGe(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_espGe"), status_code=status.HTTP_303_SEE_OTHER
    )
      
@app.post("/editEspAgendaGe/{id}")
async def editEsp_agendaGe(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp:  Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp:  Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_espGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/EspGe", response_class=HTMLResponse)
async def inicio_espGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Espeleologia/index.html", {"request": request})

@app.get("/PowerBiEspGe", response_class=HTMLResponse)
async def powerbi_espGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Espeleologia/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioEspGe", response_class=HTMLResponse)
async def calendario_espGe(request: Request):
    return templates.TemplateResponse("./Gerencia/Espeleologia/calendario.html", {"request": request, "config": config})

@app.get("/EspAgendaGe")
async def agenda_espGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Espeleologia)
        .options(joinedload(models.Demandas_Espeleologia.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Espeleologia.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Espeleologia.dth_inicio <= data_fim_dt)

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
        "./Gerencia/Espeleologia/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/EspNetprojectGe")
async def espnetprojectGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_Esp(request=request, db=db)
    
    query = db.query(models.hora_real_espeleologia)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_espeleologia.dth_inicio >= data_inicio_dt,
                models.hora_real_espeleologia.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_espeleologia.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_espeleologia.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Gerencia/Espeleologia/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_espGe/{id}")
async def edit_espGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_espeleologia)
        .filter(models.hora_real_espeleologia.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Espeleologia/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_esp_agendaGe/{id}")
async def edit_esp_agendaGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.Demandas)
        .filter(models.Demandas.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Espeleologia/edit_agenda.html", {"request": request, "demanda": projeto, "config": config}
    )

@app.get("/delete_esp_agendaGe/{id}")
async def delete_espGe(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_esp = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_esp)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_espGe"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarEspGe")
async def get_calendarespGe(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Espeleologia)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim espeleologia

#inicio humanidades

@app.post("/addHumGe")
async def addHumGe(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_humGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadHumNaoProgramadasGe", response_class=HTMLResponse)
async def CadHumNaoProgramadasGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Humanidades/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasHumGe")
async def addNaoProgramadasHumGe(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_humGe"), status_code=status.HTTP_303_SEE_OTHER
    )
     
@app.post("/editHumAgendaGe/{id}")
async def editHum_agendaGe(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp:  Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_humGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/HumGe", response_class=HTMLResponse)
async def inicio_humGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Humanidades/index.html", {"request": request})

@app.get("/PowerBiHumGe", response_class=HTMLResponse)
async def powerbi_humGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Humanidades/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioHumGe", response_class=HTMLResponse)
async def calendario_humGe(request: Request):
    return templates.TemplateResponse("./Gerencia/Humanidades/calendario.html", {"request": request, "config": config})

@app.get("/HumAgendaGe")
async def agenda_humGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Humanidades)
        .options(joinedload(models.Demandas_Humanidades.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Humanidades.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Humanidades.dth_inicio <= data_fim_dt)

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
        "./Gerencia/Humanidades/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/HumNetprojectGe")
async def espnetprojectGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_Hum(request=request, db=db)
    
    query = db.query(models.hora_real_humanidades)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_humanidades.dth_inicio >= data_inicio_dt,
                models.hora_real_humanidades.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_humanidades.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_humanidades.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Gerencia/Humanidades/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_humGe/{id}")
async def edit_humGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_humanidades)
        .filter(models.hora_real_humanidades.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Humanidades/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_hum_agendaGe/{id}")
async def edit_hum_agendaGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.Demandas)
        .filter(models.Demandas.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Humanidades/edit_agenda.html", {"request": request, "demanda": projeto, "config": config}
    )

@app.get("/delete_hum_agendaGe/{id}")
async def delete_humGe(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_hum = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_hum)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_humGe"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarHumGe")
async def get_calendarhumGe(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Humanidades)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim humanidades

#inicio MeioFisico

@app.post("/addMFGe")
async def addMFGe(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_mfGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadMFNaoProgramadasGe", response_class=HTMLResponse)
async def CadMFNaoProgramadasGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/MeioFisico/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasMFGe")
async def addNaoProgramadasMFGe(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_mfGe"), status_code=status.HTTP_303_SEE_OTHER
    )
             
@app.post("/editMFAgendaGe/{id}")
async def editMF_agendaGe(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_mfGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/MFGe", response_class=HTMLResponse)
async def inicio_mfGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/MeioFisico/index.html", {"request": request})

@app.get("/PowerBiMFGe", response_class=HTMLResponse)
async def powerbi_mfGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/MeioFisico/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioMFGe", response_class=HTMLResponse)
async def calendario_mfGe(request: Request):
    return templates.TemplateResponse("./Gerencia/MeioFisico/calendario.html", {"request": request, "config": config})

@app.get("/MFAgendaGe")
async def agenda_mfGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_MeioFisico)
        .options(joinedload(models.Demandas_MeioFisico.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_MeioFisico.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_MeioFisico.dth_inicio <= data_fim_dt)

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
        "./Gerencia/MeioFisico/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/MFNetprojectGe")
async def mfnetprojectGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_MF(request=request, db=db)
    
    query = db.query(models.hora_real_mfisico)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_mfisico.dth_inicio >= data_inicio_dt,
                models.hora_real_mfisico.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_mfisico.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_mfisico.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Gerencia/MeioFisico/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_mfGe/{id}")
async def edit_mfGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_mfisico)
        .filter(models.hora_real_mfisico.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/MeioFisico/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_mf_agendaGe/{id}")
async def edit_mf_agendaGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.Demandas)
        .filter(models.Demandas.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/MeioFisico/edit_agenda.html", {"request": request, "demanda": projeto, "config": config}
    )

@app.get("/delete_mf_agendaGe/{id}")
async def delete_mfGe(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_mf = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_mf)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_mfGe"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarMFGe")
async def get_calendarmfGe(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_MeioFisico)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim MeioFisico

#inicio Modelagens

@app.post("/addModGe")
async def addModGe(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_modGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadModNaoProgramadasGe", response_class=HTMLResponse)
async def CadModNaoProgramadasGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Modelagens/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasModGe")
async def addNaoProgramadasModGe(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return templates.TemplateResponse(
        "./Gerencia/Modelagens/agenda.html",
        {
            "config": config,
            "request": request,
        },
    )
         
@app.post("/editModAgendaGe/{id}")
async def editMod_agendaGe(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_modGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/ModGe", response_class=HTMLResponse)
async def inicio_modGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Modelagens/index.html", {"request": request})

@app.get("/PowerBiModGe", response_class=HTMLResponse)
async def powerbi_modGe(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Modelagens/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioModGe", response_class=HTMLResponse)
async def calendario_modGe(request: Request):
    return templates.TemplateResponse("./Gerencia/Modelagens/calendario.html", {"request": request, "config": config})

@app.get("/ModAgendaGe")
async def agenda_modGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Modelagens)
        .options(joinedload(models.Demandas_Modelagens.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Modelagens.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Modelagens.dth_inicio <= data_fim_dt)

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
        "./Gerencia/Modelagens/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )


@app.get("/ModNetprojectGe")
async def modnetprojectGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_Mod(request=request, db=db)
    
    query = db.query(models.hora_real_mmodelagens)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_mmodelagens.dth_inicio >= data_inicio_dt,
                models.hora_real_mmodelagens.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_mmodelagens.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_mmodelagens.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Gerencia/Modelagens/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_modGe/{id}")
async def edit_modGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_mmodelagens)
        .filter(models.hora_real_mmodelagens.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Modelagens/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_mod_agendaGe/{id}")
async def edit_mod_agendaGe(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.Demandas)
        .filter(models.Demandas.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Modelagens/edit_agenda.html", {"request": request, "demanda": projeto, "config": config}
    )

@app.get("/delete_mod_agendaGe/{id}")
async def delete_modGe(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_mod = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_mod)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_modGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CalendarModGe")
async def get_calendarmodGe(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Modelagens)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim Modelagens

#iniocio BioGe


@app.get("/Gerencia")
async def gerencia(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/index.html", {"request": request, "config": config})


@app.get("/CadBioNaoProgramadasGe", response_class=HTMLResponse)
async def CadBioNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Biodiversidade/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addBioGe")
async def addBio(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
    horas_np=horasNP,
    status=status_projeto,
    n_hora_hub=horas,
    dth_fim=dth_fim,
    dth_inicio=dth_inicio,
    dtfimnp=dtfimnp,
    hub=hub,
    titulo=titulo,
    responsavel=responsavel,
    projeto=projeto,
    dtinicionp=dtinicionp,
    atividade=atividade,
    cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_bioGe"), status_code=status.HTTP_303_SEE_OTHER
    )
        
@app.post("/editBioAgendaGe/{id}")
async def editBio_agenda(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp:  Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp:  Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_bioGe"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/BioGe", response_class=HTMLResponse)
async def inicio_bio(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Biodiversidade/index.html", {"request": request})

@app.get("/PowerBiBioGe", response_class=HTMLResponse)
async def powerbi_bio(
    request: Request
):
    return templates.TemplateResponse("./Gerencia/Biodiversidade/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioBioGe", response_class=HTMLResponse)
async def calendario_bio(request: Request):
    return templates.TemplateResponse("./Gerencia/Biodiversidade/calendario.html", {"request": request, "config": config})

@app.get("/BioAgendaGe")
async def agenda_bioGe(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Biodiversidade)
        .options(joinedload(models.Demandas_Biodiversidade.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Biodiversidade.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Biodiversidade.dth_inicio <= data_fim_dt)

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
        "./Gerencia/Biodiversidade/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/BioNetprojectGe")
async def bionetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    data_calendar = await get_Demandas_Bio(request=request, db=db)
    
    query = db.query(models.hora_real_biodiversidade)
    
    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
  
    if data_inicio and data_fim:
        query = query.filter(
            and_(
                models.hora_real_biodiversidade.dth_inicio >= data_inicio_dt,
                models.hora_real_biodiversidade.dth_prevista <= data_fim_dt
            )
        )
    elif data_inicio:
        query = query.filter(models.hora_real_biodiversidade.dth_inicio >= data_inicio_dt)
    elif data_fim:
        query = query.filter(models.hora_real_biodiversidade.dth_prevista <= data_fim_dt)
        
    demanda = query.all()
    
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]
    
    return templates.TemplateResponse(
        "./Gerencia/Biodiversidade/netproject.html",
        {
            "config": config,
            "request": request,
            "data":  list(data),
        },
    )   

@app.get("/edit_bioGe/{id}")
async def edit_bio(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.hora_real_biodiversidade)
        .filter(models.hora_real_biodiversidade.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Biodiversidade/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_bio_agendaGe/{id}")
async def edit_bio_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.Demandas)
        .filter(models.Demandas.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "./Gerencia/Biodiversidade/edit_agenda.html", {"request": request, "demanda": projeto, "config": config}
    )

@app.get("/delete_bio_agendaGe/{id}")
async def delete_bio(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_bio = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_bio)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_bioGe"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/CalendarBioGe")
async def get_calendarbio(
    request: Request, 
    db: Session = Depends(get_db), 
):
    query = db.query(models.Demandas_Biodiversidade)

    result = query.all()

    data = [
        {
            "title": r.atividade,
            "pai": r.titulo,
            "colaborador": r.responsavel,
            "start": r.dth_inicio,
            "end": r.dth_fim,
            "projeto": r.projeto,
        }
        for r in result
    ]

    return data
#fim bio

#fim admin

@app.get("/MeM")
async def MeM(
    request: Request
):
    return templates.TemplateResponse("./mem.html", {"request": request, "config": config})

#inicio nao programadas
@app.get("/CadNaoProgramadas/{hub}")
async def CadNaoProgramadas(
    request: Request,
    hub: str,
    db: Session = Depends(get_db),
):
    mapa_models = {
        "Arq": ("AquisicaoArq", "./Arqueologia/aquisicao.html"),
        "ArqGe": ("AquisicaoArq", "./Gerencia/Arqueologia/aquisicao.html"),
        "Bio": ("AquisicaoBio", "./Biodiversidade/aquisicao.html"),
        "BioGe": ("AquisicaoBio", "./Gerencia/Biodiversidade/aquisicao.html"),
        "Esp": ("AquisicaoEsp", "./Espeleologia/aquisicao.html"),
        "EspGe": ("AquisicaoEsp", "./Gerencia/Espeleologia/aquisicao.html"),
        "Geo": ("AquisicaoGeo", "./Geo/aquisicao.html"),
        "GeoGe": ("AquisicaoGeo", "./Gerencia/Geo/aquisicao.html"),
        "Hum": ("AquisicaoHum", "./Humanidades/aquisicao.html"),
        "HumGe": ("AquisicaoHum", "./Gerencia/Humanidades/aquisicao.html"),
        "MF": ("AquisicaoMF", "./MeioFisico/aquisicao.html"),
        "MFGe": ("AquisicaoMF", "./Gerencia/MeioFisico/aquisicao.html"),
        "Mod": ("AquisicaoMod", "./Modelagens/aquisicao.html"),
        "ModGe": ("AquisicaoMod", "./Gerencia/Modelagens/aquisicao.html"),
    }

    model, caminho = mapa_models.get(hub, (None, None))

    if not model or not caminho:
        return {"error": f"O hub '{hub}' não é válido."}

    ModelClass = getattr(models, model, None)

    if ModelClass is None:
        return {"error": f"O modelo '{model}' não foi encontrado."}

    query = db.query(ModelClass)
    demanda = query.all()

    return templates.TemplateResponse(
        caminho,
        {
            "config": config,
            "request": request,
            "data": demanda,
        },
    )

@app.get("/CadArqNaoProgramadas", response_class=HTMLResponse)
async def CadArqNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Arqueologia/naoprogramadas.html", {"request": request, "config": config})

#fim nao programadas

#inicio aquisições
@app.get("/Aquisicao/{hub}")
async def aquisicao(
    request: Request,
    hub: str,
    db: Session = Depends(get_db),
):
    mapa_models = {
        "Arq": ("AquisicaoArq", "./Arqueologia/aquisicao.html"),
        "ArqGe": ("AquisicaoArq", "./Gerencia/Arqueologia/aquisicao.html"),
        "Bio": ("AquisicaoBio", "./Biodiversidade/aquisicao.html"),
        "BioGe": ("AquisicaoBio", "./Gerencia/Biodiversidade/aquisicao.html"),
        "Esp": ("AquisicaoEsp", "./Espeleologia/aquisicao.html"),
        "EspGe": ("AquisicaoEsp", "./Gerencia/Espeleologia/aquisicao.html"),
        "Geo": ("AquisicaoGeo", "./Geo/aquisicao.html"),
        "GeoGe": ("AquisicaoGeo", "./Gerencia/Geo/aquisicao.html"),
        "Hum": ("AquisicaoHum", "./Humanidades/aquisicao.html"),
        "HumGe": ("AquisicaoHum", "./Gerencia/Humanidades/aquisicao.html"),
        "MF": ("AquisicaoMF", "./MeioFisico/aquisicao.html"),
        "MFGe": ("AquisicaoMF", "./Gerencia/MeioFisico/aquisicao.html"),
        "Mod": ("AquisicaoMod", "./Modelagens/aquisicao.html"),
        "ModGe": ("AquisicaoMod", "./Gerencia/Modelagens/aquisicao.html"),
    }

    model, caminho = mapa_models.get(hub, (None, None))

    if not model or not caminho:
        return {"error": f"O hub '{hub}' não é válido."}

    ModelClass = getattr(models, model, None)

    if ModelClass is None:
        return {"error": f"O modelo '{model}' não foi encontrado."}

    query = db.query(ModelClass)
    demanda = query.all()

    return templates.TemplateResponse(
        caminho,
        {
            "config": config,
            "request": request,
            "data": demanda,
        },
    )

#fim aquisições




#inicio coordenacao

@app.post("/addGestao")
async def addGestao(
    request: Request,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp: date = Form(...),
    hub: str = Form(...),
    cod_projeto: int = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp: date = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=horasNP,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=dtfimnp,
        hub=hub,
        titulo=titulo,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=dtinicionp,
        atividade=atividade,
        cod_projeto=cod_projeto,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_gestao"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/CadGestaoNaoProgramadas", response_class=HTMLResponse)
async def CadGestaoNaoProgramadas(
    request: Request
):
    return templates.TemplateResponse("./Gestao/naoprogramadas.html", {"request": request, "config": config})

@app.post("/addNaoProgramadasGestao")
async def addNaoProgramadasGestao(
    request: Request,
    atividade: str = Form(...),
    hub: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dth_inicio: str = Form(...),
    dth_fim: str = Form(...),
    horas: str = Form(...),
    observacao: str = Form(...),
    status_projeto: str = Form(...),
    db: Session = Depends(get_db),
):
    demanda = models.Demandas(
        horas_np=None,
        status=status_projeto,
        n_hora_hub=horas,
        dth_fim=dth_fim,
        dth_inicio=dth_inicio,
        dtfimnp=None,
        hub=hub,
        titulo=observacao,
        responsavel=responsavel,
        projeto=projeto,
        dtinicionp=None,
        atividade=atividade,
        cod_projeto=None,
    )
    db.add(demanda)
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_gestao"), status_code=status.HTTP_303_SEE_OTHER
    )
        
@app.post("/editGestaoAgenda/{id}")
async def editGestao_agenda(
    request: Request,
    id: int,
    status_projeto: str = Form(...),
    horas: str = Form(...),
    horasNP: str = Form(...),
    dth_fim: date = Form(...),
    dth_inicio: date = Form(...),
    dtfimnp:  Optional[date] = Form(None),
    hub: str = Form(...),
    cod_projeto: str = Form(...),
    atividade: str = Form(...),
    titulo: str = Form(...),
    responsavel: str = Form(...),
    projeto: str = Form(...),
    dtinicionp:  Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    
    demanda = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    demanda.horas_np=horasNP
    demanda.status=status_projeto
    demanda.n_hora_hub=horas
    demanda.dth_fim=dth_fim
    demanda.dth_inicio=dth_inicio
    demanda.dtfimnp=dtfimnp
    demanda.hub=hub
    demanda.titulo=titulo
    demanda.responsavel=responsavel
    demanda.projeto=projeto
    demanda.dtinicionp=dtinicionp
    demanda.atividade=atividade
    demanda.cod_projeto=cod_projeto
    
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("agenda_gestao"), status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/Gestao", response_class=HTMLResponse)
async def inicio_gestao(
    request: Request
):
    return templates.TemplateResponse("./Gestao/index.html", {"request": request})

@app.get("/PowerBiGestao", response_class=HTMLResponse)
async def powerbi_gestao(
    request: Request
):
    return templates.TemplateResponse("./Gestao/powerbi.html", {"request": request, "config": config})

@app.get("/CalendarioGestao", response_class=HTMLResponse)
async def calendario_gestao(request: Request):
    return templates.TemplateResponse("Biodiversidade/calendario.html", {"request": request, "config": config})

@app.get("/GestaoAgenda")
async def agenda_gestao(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Gestao)
        .options(joinedload(models.Demandas_Gestao.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Gestao.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Gestao.dth_inicio <= data_fim_dt)

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
        "./Gestao/agenda.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
    )

@app.get("/GestaoNetproject")
async def gestaonetproject(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    # Logando os parâmetros recebidos
    logging.info(f"Parâmetros recebidos - data_inicio: {data_inicio}, data_fim: {data_fim}")
    
    # Converta as strings de data em objetos datetime
    data_inicio_dt = None
    data_fim_dt = None
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            logging.info(f"data_inicio convertido: {data_inicio_dt}")
        except ValueError as e:
            logging.error(f"Erro ao converter data_inicio: {e}")
            
    if data_fim:
        try:
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
            logging.info(f"data_fim convertido: {data_fim_dt}")
        except ValueError as e:
            logging.error(f"Erro ao converter data_fim: {e}")
    
    # Realize a consulta ao banco de dados
    query = db.query(models.Gestao)
    
    # Filtros de data
    if data_inicio_dt and data_fim_dt:
        query = query.filter(
            models.Gestao.dth_inicio >= data_inicio_dt,
            models.Gestao.dth_prevista <= data_fim_dt
        )
    elif data_inicio_dt:
        query = query.filter(models.Gestao.dth_inicio >= data_inicio_dt)
    elif data_fim_dt:
        query = query.filter(models.Gestao.dth_prevista <= data_fim_dt)
    
    demanda = query.all()

    # Logando a quantidade de resultados encontrados
    logging.info(f"Quantidade de resultados encontrados: {len(demanda)}")

    # Formatando as datas
    for item in demanda:
        item.dth_inicio = item.dth_inicio.strftime("%d-%m-%Y")
        item.dth_prevista = item.dth_prevista.strftime("%d-%m-%Y")

    # Comparação adicional, se necessário
    data_calendar = await get_Demandas_Gestao(request=request, db=db)
    ids_calendar = {(item.cod_projeto, item.responsavel) for item in data_calendar}
    ids_another = {(item.cod_projeto, item.nom_usuario) for item in demanda}

    differences_ids = ids_another - ids_calendar

    data = [
        item for item in demanda if (item.cod_projeto, item.nom_usuario) in differences_ids
    ]


    return templates.TemplateResponse(
        "./Gestao/netproject.html",
        {
            "config": config,
            "request": request,
            "data": list(data),
        },
    )

@app.get("/edit_gestao/{id}")
async def edit_gestao(request: Request, id: str, db: Session = Depends(get_db)):
    projeto = (
        db.query(models.Gestao)
        .filter(models.Gestao.id == id)
        .first()
    )
    return templates.TemplateResponse(
        "/Gestao/edit.html", {"request": request, "demanda": projeto, "config": config}
    )
    
@app.get("/edit_gestao_agenda/{id}")
async def edit_gestao_agenda(request: Request, id: str, db: Session = Depends(get_db)):
    # Consulta na tabela Demandas para pegar o cod_projeto e nom_usuario
    projeto = db.query(models.Demandas).filter(models.Demandas.id == id).first()

    if projeto:
        cod_projeto1 = projeto.cod_projeto  # Atribuindo o valor de cod_projeto
        nom_usuario1 = projeto.responsavel  # Atribuindo o valor de nom_usuario
    else:
        cod_projeto1 = None  # Caso não encontre o projeto, define como None
        nom_usuario1 = None  # Caso não encontre o projeto, define como None
    
    # Verificando os valores atribuídos
    print(f"Valor de cod_projeto1: {cod_projeto1}")
    print(f"Valor de nom_usuario1: {nom_usuario1}")

    # Consulta na tabela hora_real_usuario utilizando os valores dinâmicos de cod_projeto1 e nom_usuario1
    netproject = (
        db.query(models.Gestao)
        .filter(
            models.Gestao.cod_projeto == cod_projeto1,  # Filtro para cod_projeto
            models.Gestao.nom_usuario == nom_usuario1   # Filtro para nom_usuario
        )
        .first()
    )

    # Verificando o resultado da consulta
    print(f'netproject: {netproject}')
    
    return templates.TemplateResponse(
        "/Gestao/edit_agenda.html", {"request": request, "demanda": projeto, "netproject": netproject, "config": config}
    )

@app.get("/delete_gestao_agenda/{id}")
async def delete_gestao(request: Request, id: str, db: Session = Depends(get_db)):
    demanda_agenda_gestao = db.query(models.Demandas).filter(models.Demandas.id == id).first()
    db.delete(demanda_agenda_gestao)
    db.commit()
    return RedirectResponse(url=app.url_path_for("agenda_gestao"), status_code=status.HTTP_303_SEE_OTHER)


#fim coordenacao

@app.get("/teste")
async def agenda_hum(
    request: Request,
    db: Session = Depends(get_db),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
):
    query = (
        db.query(models.Demandas_Humanidades)
        .options(joinedload(models.Demandas_Humanidades.hora_real_usuario))  # Carrega o relacionamento
    )

    if data_inicio:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        query = query.filter(models.Demandas_Humanidades.dth_fim >= data_inicio_dt)

    if data_fim:
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
        query = query.filter(models.Demandas_Humanidades.dth_inicio <= data_fim_dt)

    demandas = query.all()

    data = []
    for demanda in demandas:
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
            "dtinicionp": demanda.dtinicionp.strftime("%d-%m-%Y") if demanda.dtinicionp else None,
            "dtfimnp": demanda.dtfimnp.strftime("%d-%m-%Y") if demanda.dtfimnp else None
        })
        
    return templates.TemplateResponse(
        "./Humanidades/teste.html",
        {
            "config": config,
            "request": request,
            "data": data,
        },
        )