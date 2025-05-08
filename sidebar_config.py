from hubs import mapa_templates, mapa_aquisicao

def gerar_sidebar_por_hub():
    sidebar = {}

    rotas_comuns = {
        "netproject": ("Netproject", "fa fa-database"),
        "agenda": ("Agenda", "fa fa-calendar"),
        "powerbi": ("PowerBi", "fa fa-chart-bar"),
        "calendario": ("Calendario", "fa fa-calendar-alt"),
    }

    # Caso especial para "gerencia"
    itens_gerencia = []

    for hub, templates in mapa_templates.items():
        if len(templates) <= 1:
            continue

        itens_hub = [{"name": "Início", "href": "/", "icon": "fa fa-home"}]

        for chave, (label, icon) in rotas_comuns.items():
            if chave in templates:
                rota = f"/{label}/{hub}"
                itens_hub.append({"name": label, "href": rota, "icon": icon})

        if hub in mapa_aquisicao:
            itens_hub.append({
                "name": "Aquisições",
                "href": f"/Aquisicao/{hub}",
                "icon": "fa fa-shopping-cart"
            })

        # Adiciona ao sidebar normal
        sidebar[hub.upper()] = itens_hub

        # Verifica se o hub deve ser adicionado à gerência
        if hub.capitalize().endswith("GE"):
            # Adiciona ao submenu de gerência apenas hubs que terminam com "GE"
            itens_gerencia.append({
                "name": hub.upper(),
                "icon": "fa fa-building",
                "submenu": itens_hub  # Submenu específico do hub
            })

    # Adiciona a entrada especial para GERENCIA
    sidebar["Gerencia"] = itens_gerencia

    return sidebar

SIDEBAR_MENUS = gerar_sidebar_por_hub()

