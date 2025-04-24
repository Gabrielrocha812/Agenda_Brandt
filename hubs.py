import models

# Dicionário com models de demanda
mapa_models_demanda = {
    "Arq": models.Demandas_Arqueologia,
    "ArqGe": models.Demandas_Arqueologia,
    "Bio": models.Demandas_Biodiversidade,
    "BioGe": models.Demandas_Biodiversidade,
    "Esp": models.Demandas_Espeleologia,
    "EspGe": models.Demandas_Espeleologia,
    "Geo": models.Demandas_Geo,
    "GeoGe": models.Demandas_Geo,
    "Hum": models.Demandas_Humanidades,
    "HumGe": models.Demandas_Humanidades,
    "MF": models.Demandas_MeioFisico,
    "MFGe": models.Demandas_MeioFisico,
    "Mod": models.Demandas_Modelagens,
    "ModGe": models.Demandas_Modelagens,
}

# Dicionário com models de horas reais por hub
mapa_models_hora_real = {
    "Arq": models.hora_real_arqueologia,
    "ArqGe": models.hora_real_arqueologia,
    "Bio": models.hora_real_biodiversidade,
    "BioGe": models.hora_real_biodiversidade,
    "Esp": models.hora_real_espeleologia,
    "EspGe": models.hora_real_espeleologia,
    "Geo": models.hora_real_geo,
    "GeoGe": models.hora_real_geo,
    "Hum": models.hora_real_humanidades,
    "HumGe": models.hora_real_humanidades,
    "MF": models.hora_real_mfisico,
    "MFGe": models.hora_real_mfisico,
    "Mod": models.hora_real_mmodelagens,
    "ModGe": models.hora_real_mmodelagens,
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
    "ArqGe": {
        "agenda": "./Gerencia/Arqueologia/agenda.html",
        "edit": "./Gerencia/Arqueologia/edit_agenda.html",
        "netproject": "./Gerencia/Arqueologia/netproject.html",
        "naoprogramadas": "./Gerencia/Arqueologia/naoprogramadas.html",
        "calendario": "./Gerencia/Arqueologia/calendario.html",
        "powerbi": "./Gerencia/Arqueologia/PowerBi.html",
        "index": "./Gerencia/Arqueologia/index.html",
        "edit_simples": "./Gerencia/Arqueologia/edit.html",
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
    "BioGe": {
        "agenda": "./Gerencia/Biodiversidade/agenda.html",
        "edit": "./Gerencia/Biodiversidade/edit_agenda.html",
        "netproject": "./Gerencia/Biodiversidade/netproject.html",
        "naoprogramadas": "./Gerencia/Biodiversidade/naoprogramadas.html",
        "calendario": "./Gerencia/Biodiversidade/calendario.html",
        "powerbi": "./Gerencia/Biodiversidade/PowerBi.html",
        "index": "./Gerencia/Biodiversidade/index.html",
        "edit_simples": "./Gerencia/Biodiversidade/edit.html",
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
    "EspGe": {
        "agenda": "./Gerencia/Espeleologia/agenda.html",
        "edit": "./Gerencia/Espeleologia/edit_agenda.html",
        "netproject": "./Gerencia/Espeleologia/netproject.html",
        "naoprogramadas": "./Gerencia/Espeleologia/naoprogramadas.html",
        "calendario": "./Gerencia/Espeleologia/calendario.html",
        "powerbi": "./Gerencia/Espeleologia/PowerBi.html",
        "index": "./Gerencia/Espeleologia/index.html",
        "edit_simples": "./Gerencia/Espeleologia/edit.html",
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
    "GeoGe": {
        "agenda": "./Gerencia/Geo/agenda.html",
        "edit": "./Gerencia/Geo/edit_agenda.html",
        "netproject": "./Gerencia/Geo/netproject.html",
        "naoprogramadas": "./Gerencia/Geo/naoprogramadas.html",
        "calendario": "./Gerencia/Geo/calendario.html",
        "powerbi": "./Gerencia/Geo/PowerBi.html",
        "index": "./Gerencia/Geo/index.html",
        "edit_simples": "./Gerencia/Geo/edit.html",
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
    "HumGe": {
        "agenda": "./Gerencia/Humanidades/agenda.html",
        "edit": "./Gerencia/Humanidades/edit_agenda.html",
        "netproject": "./Gerencia/Humanidades/netproject.html",
        "naoprogramadas": "./Gerencia/Humanidades/naoprogramadas.html",
        "calendario": "./Gerencia/Humanidades/calendario.html",
        "powerbi": "./Gerencia/Humanidades/PowerBi.html",
        "index": "./Gerencia/Humanidades/index.html",
        "edit_simples": "./Gerencia/Humanidades/edit.html",
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
    "MFGe": {
        "agenda": "./Gerencia/MeioFisico/agenda.html",
        "edit": "./Gerencia/MeioFisico/edit_agenda.html",
        "netproject": "./Gerencia/MeioFisico/netproject.html",
        "naoprogramadas": "./Gerencia/MeioFisico/naoprogramadas.html",
        "calendario": "./Gerencia/MeioFisico/calendario.html",
        "powerbi": "./Gerencia/MeioFisico/PowerBi.html",
        "index": "./Gerencia/MeioFisico/index.html",
        "edit_simples": "./Gerencia/MeioFisico/edit.html",
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
    "ModGe": {
        "agenda": "./Gerencia/Modelagens/agenda.html",
        "edit": "./Gerencia/Modelagens/edit_agenda.html",
        "netproject": "./Gerencia/Modelagens/netproject.html",
        "naoprogramadas": "./Gerencia/Modelagens/naoprogramadas.html",
        "calendario": "./Gerencia/Modelagens/calendario.html",
        "powerbi": "./Gerencia/Modelagens/PowerBi.html",
        "index": "./Gerencia/Modelagens/index.html",
        "edit_simples": "./Gerencia/Modelagens/edit.html",
    },
    "Gerencia": {
        "index": "./Gerencia/index.html",
    },
    "MeM": {
        "index": "./mem.html",
    }
}

mapa_aquisicao = {
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

# Helpers utilitários

def get_model_demanda_by_hub(hub: str):
    return mapa_models_demanda.get(hub)

def get_model_hora_real_by_hub(hub: str):
    return mapa_models_hora_real.get(hub)

def get_templates_by_hub(hub: str):
    return mapa_templates.get(hub, {})