import models
import sidebar_config

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
    "GestaoGe": models.Demandas_Gestao,
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
    "GestaoGe": models.Gestao
}

# Templates de visualização (agenda, edição, etc.)
mapa_templates = {
    "Arq": {
        "agenda": "./Arqueologia/agenda.html",
        "edit": "./Arqueologia/edit_agenda.html",
        "netproject": "./Arqueologia/netproject.html",
        "naoprogramadas": "./Arqueologia/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Arqueologia/PowerBi.html",
        "index": "./Arqueologia/index.html",
        "edit_simples": "./Arqueologia/edit.html",
    },
    "ArqGe": {
        "agenda": "./Gerencia/Arqueologia/agenda.html",
        "edit": "./Gerencia/Arqueologia/edit_agenda.html",
        "netproject": "./Gerencia/Arqueologia/netproject.html",
        "naoprogramadas": "./Gerencia/Arqueologia/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Gerencia/Arqueologia/PowerBi.html",
        "index": "./Gerencia/Arqueologia/index.html",
        "edit_simples": "./Gerencia/Arqueologia/edit.html",
    },
    "Bio": {
        "agenda": "./Biodiversidade/agenda.html",
        "edit": "./Biodiversidade/edit_agenda.html",
        "netproject": "./Biodiversidade/netproject.html",
        "naoprogramadas": "./Biodiversidade/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Biodiversidade/PowerBi.html",
        "index": "./Biodiversidade/index.html",
        "edit_simples": "./Biodiversidade/edit.html",
    },
    "BioGe": {
        "agenda": "./Gerencia/Biodiversidade/agenda.html",
        "edit": "./Gerencia/Biodiversidade/edit_agenda.html",
        "netproject": "./Gerencia/Biodiversidade/netproject.html",
        "naoprogramadas": "./Gerencia/Biodiversidade/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Gerencia/Biodiversidade/PowerBi.html",
        "index": "./Gerencia/Biodiversidade/index.html",
        "edit_simples": "./Gerencia/Biodiversidade/edit.html",
    },
    "Esp": {
        "agenda": "./Espeleologia/agenda.html",
        "edit": "./Espeleologia/edit_agenda.html",
        "netproject": "./Espeleologia/netproject.html",
        "naoprogramadas": "./Espeleologia/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Espeleologia/PowerBi.html",
        "index": "./Espeleologia/index.html",
        "edit_simples": "./Espeleologia/edit.html",
    },
    "EspGe": {
        "agenda": "./Gerencia/Espeleologia/agenda.html",
        "edit": "./Gerencia/Espeleologia/edit_agenda.html",
        "netproject": "./Gerencia/Espeleologia/netproject.html",
        "naoprogramadas": "./Gerencia/Espeleologia/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Gerencia/Espeleologia/PowerBi.html",
        "index": "./Gerencia/Espeleologia/index.html",
        "edit_simples": "./Gerencia/Espeleologia/edit.html",
    },
    "Geo": {
        "agenda": "./Geo/agenda.html",
        "edit": "./Geo/edit_agenda.html",
        "netproject": "./Geo/netproject.html",
        "naoprogramadas": "./Geo/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Geo/PowerBi.html",
        "index": "./Geo/index.html",
        "edit_simples": "./Geo/edit.html",
    },
    "GeoGe": {
        "agenda": "./Gerencia/Geo/agenda.html",
        "edit": "./Gerencia/Geo/edit_agenda.html",
        "netproject": "./Gerencia/Geo/netproject.html",
        "naoprogramadas": "./Gerencia/Geo/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Gerencia/Geo/PowerBi.html",
        "index": "./Gerencia/Geo/index.html",
        "edit_simples": "./Gerencia/Geo/edit.html",
    },
    "Hum": {
        "agenda": "./Humanidades/agenda.html",
        "edit": "./Humanidades/edit_agenda.html",
        "netproject": "./Humanidades/netproject.html",
        "naoprogramadas": "./Humanidades/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Humanidades/PowerBi.html",
        "index": "./Humanidades/index.html",
        "edit_simples": "./Humanidades/edit.html",
    },
    "HumGe": {
        "agenda": "./Gerencia/Humanidades/agenda.html",
        "edit": "./Gerencia/Humanidades/edit_agenda.html",
        "netproject": "./Gerencia/Humanidades/netproject.html",
        "naoprogramadas": "./Gerencia/Humanidades/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Gerencia/Humanidades/PowerBi.html",
        "index": "./Gerencia/Humanidades/index.html",
        "edit_simples": "./Gerencia/Humanidades/edit.html",
    },
    "MF": {
        "agenda": "./MeioFisico/agenda.html",
        "edit": "./MeioFisico/edit_agenda.html",
        "netproject": "./MeioFisico/netproject.html",
        "naoprogramadas": "./MeioFisico/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./MeioFisico/PowerBi.html",
        "index": "./MeioFisico/index.html",
        "edit_simples": "./MeioFisico/edit.html",
    },
    "MFGe": {
        "agenda": "./Gerencia/MeioFisico/agenda.html",
        "edit": "./Gerencia/MeioFisico/edit_agenda.html",
        "netproject": "./Gerencia/MeioFisico/netproject.html",
        "naoprogramadas": "./Gerencia/MeioFisico/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Gerencia/MeioFisico/PowerBi.html",
        "index": "./Gerencia/MeioFisico/index.html",
        "edit_simples": "./Gerencia/MeioFisico/edit.html",
    },
    "Mod": {
        "agenda": "./Modelagens/agenda.html",
        "edit": "./Modelagens/edit_agenda.html",
        "netproject": "./Modelagens/netproject.html",
        "naoprogramadas": "./Modelagens/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Modelagens/PowerBi.html",
        "index": "./Modelagens/index.html",
        "edit_simples": "./Modelagens/edit.html",
    },
    "ModGe": {
        "agenda": "./Gerencia/Modelagens/agenda.html",
        "edit": "./Gerencia/Modelagens/edit_agenda.html",
        "netproject": "./Gerencia/Modelagens/netproject.html",
        "naoprogramadas": "./Gerencia/Modelagens/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Gerencia/Modelagens/PowerBi.html",
        "index": "./Gerencia/Modelagens/index.html",
        "edit_simples": "./Gerencia/Modelagens/edit.html",
    },
    "MeM": {
        "index": "./mem.html",
    },
    "GestaoGe": {
        "agenda": "./Gestao/agenda.html",
        "edit": "./Gestao/edit_agenda.html",
        "netproject": "./Gestao/netproject.html",
        "naoprogramadas": "./Gestao/naoprogramadas.html",
        "calendario": "/calendario.html",
        "powerbi": "./Gestao/PowerBi.html",
        "index": "./Gestao/index.html",
        "edit_simples": "./Gestao/edit.html",
    },
    "Info": {
        "agenda": None,
        "edit": None,
        "netproject": None,
        "naoprogramadas": None,
        "calendario":None,
        "powerbi": None,
        "index": None,
        "edit_simples": None,
    },
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

nomes_hub_legivel_base = {
    "Arq": "Arqueologia",
    "Bio": "Biodiversidade",
    "Esp": "Espeleologia",
    "Geo": "Geointeligência",
    "Hum": "Humanidades",
    "MF": "Meio Físico",
    "Mod": "Modelagens",
    "Gerencia": "Gerência",
    "Gestao": "Gestão"
}

powerbi_links = {
    "Arq": "https://app.powerbi.com/view?r=eyJrIjoiNzVmYjU1MzEtMDE0NC00MzJlLWE5MjItMDlkY2FmNTkwMWZjIiwidCI6ImJiOTQ0OGUxLWE3YWMtNDQ0MC1iM2YyLTMxZGUwNzFhY2UwNyJ9",
    "Bio": "https://app.powerbi.com/view?r=eyJrIjoiOGUwOWY0NGItOTY0OC00OTBlLTkwYzctNTBhYjdmYjY4OWEyIiwidCI6ImJiOTQ0OGUxLWE3YWMtNDQ0MC1iM2YyLTMxZGUwNzFhY2UwNyJ9",
    "Esp": "https://app.powerbi.com/view?r=eyJrIjoiODk4NDUwZmItZTA1YS00ZmIzLWI4ODUtZDk2YTQzYmEyNDNkIiwidCI6ImJiOTQ0OGUxLWE3YWMtNDQ0MC1iM2YyLTMxZGUwNzFhY2UwNyJ9",
    "Geo": "https://app.powerbi.com/view?r=eyJrIjoiZmMxNDFjMzYtMzIxNS00YWZjLWIxNzYtZmFmOTJmOTVjMGVhIiwidCI6ImJiOTQ0OGUxLWE3YWMtNDQ0MC1iM2YyLTMxZGUwNzFhY2UwNyJ9",
    "Hum": "https://app.powerbi.com/view?r=eyJrIjoiODlmZGNkMDItNWIzYi00YzBiLTlhNWItM2E1NmE2MmQ0OThiIiwidCI6ImJiOTQ0OGUxLWE3YWMtNDQ0MC1iM2YyLTMxZGUwNzFhY2UwNyJ9",
    "MF": "https://app.powerbi.com/view?r=eyJrIjoiMWZkNjk4NjItOTA4Zi00NDkwLTkwYmItM2Y2NjUxNjkyZWE4IiwidCI6ImJiOTQ0OGUxLWE3YWMtNDQ0MC1iM2YyLTMxZGUwNzFhY2UwNyJ9",
    "GestaoGe": "https://app.powerbi.com/view?r=eyJrIjoiY2UwNDRlYWItZjQ2MS00MGMzLWE3OWYtMWY3YzFjNTBiYTIzIiwidCI6ImJiOTQ0OGUxLWE3YWMtNDQ0MC1iM2YyLTMxZGUwNzFhY2UwNyJ9",
    "Mod": "https://app.powerbi.com/view?r=eyJrIjoiYzk2NDk2OWEtOGZmOS00YjZjLThhYjgtODgwYTVhYTQ1YzE1IiwidCI6ImJiOTQ0OGUxLWE3YWMtNDQ0MC1iM2YyLTMxZGUwNzFhY2UwNyJ9",
}       

colaboradores_hubs = {
    "Arq": [
        "Deborah Lima Duarte Talim",
        "Thiago Hycaro Santos Neves",
        "Valdiney Amaral Leite",
    ],
    "Bio": [
        "Bianca Vidigal Mendes",
        "Estefania Isabel Pereira",
        "Lucas Jesus da Silveira",
        "Maria José Pinheiro Anacléto",
        "Lorena Anne Santos do Nascimento",
        "Rodrigo Morais Pessoa",
        "Ronei Rosa dos Santos",
    ],
    "Esp": [
        "Amailton Araujo Pedrosa",
        "Antonio Ribeiro Lima",
        "Breno Felipe Teixeira Gomes Melo",
        "Carleandro da Paixao Araujo",
        "Diogo Henrique Granado Checchia",
        "Diones Dionisio Costa",
        "Gilson Fernandes Marins",
        "Gleice de Paula Soares",
        "Guelmon Conceicao dos Santos",
        "Pedro Bernardes Machado",
        "Raimundo Ribeiro Lima",
        "Renea Rezende Lopes",
        "Thiago Ferreira Lima",
        "Valdir Ribeiro Lima",
        "Vinicius Minelli Moreira",
    ],
    "Geo": [
        "Camila Duarte Guerra",
        "Davi Daniel Fernandes Santos",
        "Gabriel Rocha Goncalves de Souza",
        "Gustavo Adolfo Tinoco Martinez",
        "Lucas Antonio Brasil Goncalves Lacerda",
        "Renato de Oliveira Marques",
        "Wellington Antonio de Oliveira Menez",
    ],
    "Hum": ["Ari Silva Gobira", "Luis Eduardo Maia Mallet"],
    "MF": [
        "Cesar Augusto Horn",
        "Fernando Antonio de Oliveira",
        "Giovanna Neusa Fagundes Marciano",
        "Marina Fonseca Cotta",
        "Vinícius Rodrigues dos Santos",
    ],
    "Mod": [
        "Brenda Ribeiro",
        "Cristiano Lisboa de Andrade",
        "Elizio Henrique da Silva Soares",
        "Rafael Felipe Terencio",
    ],
    "Gestao": ["Andre Tavares Barbosa", "Leandro Augusto de Freitas Borges", "Frank Carvalho Ferreira"],

}


def get_model_demanda_by_hub(hub: str):
    return mapa_models_demanda.get(hub)


def get_model_hora_real_by_hub(hub: str):
    return mapa_models_hora_real.get(hub)


def get_templates_by_hub(hub: str):
    return mapa_templates.get(hub, {})


def get_nome_legivel(hub: str) -> str:
    if hub.endswith("Ge"):
        base = hub[:-2]  # Remove "Ge"
        nome_base = nomes_hub_legivel_base.get(base, base)
        return f"{nome_base} Gerência"
    return nomes_hub_legivel_base.get(hub, hub)


def get_powerbi_link(hub: str) -> str:
    base = hub[:-2] if hub.endswith("Ge") else hub
    return powerbi_links.get(base, "")


def is_gerencia(hub: str) -> bool:
    return hub.endswith("Ge")


def get_sidebar_gerencia():
    return [
        {
            "name": get_nome_legivel(hub),
            "href": f"/{hub}Ge",
            "icon": "fa fa-folder",  # ou qualquer ícone padrão, se quiser
        }
        for hub in nomes_hub_legivel_base.keys()
        if hub != "Gerencia" and hub != "MeM"
    ]


def get_sidebar_by_hub(hub: str):

    return sidebar_config.SIDEBAR_MENUS.get(hub.upper(), [])


def get_colaboradores_por_hub(hub: str):
    # Verifica se o nome do hub contém parte da chave
    for key in colaboradores_hubs:
        if hub.capitalize().startswith(key.capitalize()):
            return colaboradores_hubs[key]
    return []
