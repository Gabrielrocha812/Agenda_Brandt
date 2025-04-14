import os
import re

# Diretório base
diretorio = "./templates"

alteracoes = {
    """{% endfor %}""": """{% endfor %}
                           {% endfor %}""",
}

# Lista de nomes de arquivos específicos para editar
arquivos_especificos = ["agenda.html"]

# Percorrer o diretório e suas subpastas
for raiz, subpastas, arquivos in os.walk(diretorio):
    for arquivo in arquivos:
        if arquivo in arquivos_especificos:  # Verificar se o arquivo está na lista
            caminho = os.path.join(raiz, arquivo)  # Caminho completo do arquivo
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()

            # Substituir os textos
            for antigo, novo in alteracoes.items():
                conteudo = re.sub(antigo, novo, conteudo)

            # Salvar as alterações
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)

print("Alterações concluídas!")
