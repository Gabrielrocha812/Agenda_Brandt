# hub_config.py
import models

# Dicionário com models de demanda
mapa_models_demanda = {
    "Arq": models.Demandas_Arqueologia,
    "Bio": models.Demandas_Biodiversidade,
    "Esp": models.Demandas_Espeleologia,
    "Geo": models.Demandas_Geo,
    "Hum": models.Demandas_Humanidades,
    "MF": models.Demandas_MeioFisico,
    "Mod": models.Demandas_Modelagens,
}

# Dicionário com models de horas reais por hub
mapa_models_hora_real = {
    "Arq": models.hora_real_arqueologia,
    "Bio": models.hora_real_biodiversidade,
    "Esp": models.hora_real_espeleologia,
    "Geo": models.hora_real_geo,
    "Hum": models.hora_real_humanidades,
    "MF": models.hora_real_mfisico,
    "Mod": models.hora_real_mmodelagens,
}

# Templates de visualização (agenda, edição, etc.)
mapa_templates = {
    "Arq": {
        "agenda": "./Arqueologia/agenda.html",
        "edit": "./Arqueologia/edit_agenda.html",
        "netproject": "./Arqueologia/netproject.html",
        "naoprogramadas": "./Arqueologia/naoprogramadas.html",
        "calendario": "./Arqueologia/calendario.html",
        "powerbi": "./Arqueologia/PowerBi.html",
        "index": "./Arqueologia/index.html",
        "edit_simples": "./Arqueologia/edit.html",
    },
    "Bio": {
        "agenda": "./Biodiversidade/agenda.html",
        "edit": "./Biodiversidade/edit_agenda.html",
        "netproject": "./Biodiversidade/netproject.html",
        "naoprogramadas": "./Biodiversidade/naoprogramadas.html",
        "calendario": "./Biodiversidade/calendario.html",
        "powerbi": "./Biodiversidade/PowerBi.html",
        "index": "./Biodiversidade/index.html",
        "edit_simples": "./Biodiversidade/edit.html",
    },
    "Esp": {
        "agenda": "./Espeleologia/agenda.html",
        "edit": "./Espeleologia/edit_agenda.html",
        "netproject": "./Espeleologia/netproject.html",
        "naoprogramadas": "./Espeleologia/naoprogramadas.html",
        "calendario": "./Espeleologia/calendario.html",
        "powerbi": "./Espeleologia/PowerBi.html",
        "index": "./Espeleologia/index.html",
        "edit_simples": "./Espeleologia/edit.html",
    },
    "Geo": {
        "agenda": "./Geo/agenda.html",
        "edit": "./Geo/edit_agenda.html",
        "netproject": "./Geo/netproject.html",
        "naoprogramadas": "./Geo/naoprogramadas.html",
        "calendario": "./Geo/calendario.html",
        "powerbi": "./Geo/PowerBi.html",
        "index": "./Geo/index.html",
        "edit_simples": "./Geo/edit.html",
    },
    "Hum": {
        "agenda": "./Humanidades/agenda.html",
        "edit": "./Humanidades/edit_agenda.html",
        "netproject": "./Humanidades/netproject.html",
        "naoprogramadas": "./Humanidades/naoprogramadas.html",
        "calendario": "./Humanidades/calendario.html",
        "powerbi": "./Humanidades/PowerBi.html",
        "index": "./Humanidades/index.html",
        "edit_simples": "./Humanidades/edit.html",
    },
    "MF": {
        "agenda": "./MeioFisico/agenda.html",
        "edit": "./MeioFisico/edit_agenda.html",
        "netproject": "./MeioFisico/netproject.html",
        "naoprogramadas": "./MeioFisico/naoprogramadas.html",
        "calendario": "./MeioFisico/calendario.html",
        "powerbi": "./MeioFisico/PowerBi.html",
        "index": "./MeioFisico/index.html",
        "edit_simples": "./MeioFisico/edit.html",
    },
    "Mod": {
        "agenda": "./Modelagens/agenda.html",
        "edit": "./Modelagens/edit_agenda.html",
        "netproject": "./Modelagens/netproject.html",
        "naoprogramadas": "./Modelagens/naoprogramadas.html",
        "calendario": "./Modelagens/calendario.html",
        "powerbi": "./Modelagens/PowerBi.html",
        "index": "./Modelagens/index.html",
        "edit_simples": "./Modelagens/edit.html",
    },
    "Gerencia": {
        "index": "./Gerencia/index.html",
    },
    "MeM": {
        "index": "./mem.html",
    }
}

# Helpers utilitários

def get_model_demanda_by_hub(hub: str):
    return mapa_models_demanda.get(hub)

def get_model_hora_real_by_hub(hub: str):
    return mapa_models_hora_real.get(hub)

def get_templates_by_hub(hub: str):
    return mapa_templates.get(hub, {})
