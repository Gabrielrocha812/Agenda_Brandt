from hubs import mapa_templates, mapa_aquisicao

def gerar_sidebar_por_hub():
    sidebar = {}

    rotas_comuns = {
        "netproject": ("Netproject", "fa fa-database"),
        "agenda": ("Agenda", "fa fa-calendar"),
        "powerbi": ("PowerBi", "fa fa-chart-bar"),
        "calendario": ("Calendario", "fa fa-calendar-alt"),
    }

    for hub, templates in mapa_templates.items():
        if len(templates) <= 1:
            continue

        itens = [
            {"name": "Início", "href": "/", "icon": "fa fa-home"}
        ]

        for chave, (label, icon) in rotas_comuns.items():
            if chave in templates:
                rota = f"/{label}/{hub}"  # Ex: /Netproject/Hum
                itens.append({"name": label, "href": rota, "icon": icon})

        if hub in mapa_aquisicao:
            itens.append({
                "name": "Aquisições",
                "href": f"/Aquisicao/{hub}",
                "icon": "fa fa-shopping-cart"
            })

        sidebar[hub.upper()] = itens

    return sidebar

SIDEBAR_MENUS = gerar_sidebar_por_hub()
