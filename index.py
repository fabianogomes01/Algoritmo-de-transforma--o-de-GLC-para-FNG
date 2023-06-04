def transformar_glc_para_fng(gramatica):
    # Cria um novo símbolo inicial
    nova_gramatica = ["S' -> " + gramatica[0].split('->')[0].strip()]

    # Remove regras vazias
    for regra in gramatica:
        partes = regra.split('->')
        nao_terminal = partes[0].strip()
        corpos = partes[1].split('|')

        for corpo in corpos:
            if corpo.strip() != 'λ':
                nova_gramatica.append(regra.strip())

    # Remove regras unitárias
    regras_unitarias = []
    for regra in nova_gramatica:
        partes = regra.split('->')
        if len(partes) == 2 and partes[1].strip().isupper():
            regras_unitarias.append(regra.strip())

    while regras_unitarias:
        regra_unitaria = regras_unitarias.pop(0)
        partes = regra_unitaria.split('->')
        nao_terminal = partes[0].strip()
        nao_terminal_unitario = partes[1].strip()

        for regra in nova_gramatica:
            partes = regra.split('->')
            if len(partes) == 2 and partes[0].strip() == nao_terminal_unitario:
                nova_regra = nao_terminal + " -> " + partes[1].strip()
                if nova_regra not in nova_gramatica:
                    regras_unitarias.append(nova_regra)
                    nova_gramatica.append(nova_regra)

    # Elimina símbolos inúteis
    simbolos_utilizados = []
    simbolos_utilizados.append(nova_gramatica[0].split('->')[0].strip())

    for regra in nova_gramatica:
        partes = regra.split('->')
        nao_terminal = partes[0].strip()
        corpos = partes[1].split('|')

        for corpo in corpos:
            for simbolo in corpo.strip().split():
                if simbolo.isupper():
                    simbolos_utilizados.append(simbolo)

    nova_gramatica = [regra for regra in nova_gramatica if regra.split('->')[0].strip() in simbolos_utilizados]

    nova_gramatica = [regra.replace("S'", simbolos_utilizados[0]) for regra in nova_gramatica]

    return nova_gramatica


# Exemplo de uso
gramatica = [
    "S -> AB | BCS",
    "A -> aA | C",
    "B -> bbB | b",
    "C -> cC | λ"
]

fng = transformar_glc_para_fng(gramatica)
for regra in fng:
    print(regra)
