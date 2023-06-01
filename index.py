def transform_to_greibach(glc):
    greibach = []  # Lista para armazenar as produções na FNG
    nonterminals = list(glc.keys())  # Não terminais da GLC (cópia)

    # Passo 1: Remover produções vazias
    for nt, productions in glc.items():
        if 'λ' in productions:
            glc[nt].remove('λ')
            for nt2, productions2 in glc.items():
                glc[nt2] = [p.replace(nt, '') for p in productions2]

    # Passo 2: Remover produções unitárias
    for nt in nonterminals:
        unit_productions = [p for p in glc[nt] if len(p) == 1 and p.isupper()]
        while unit_productions:
            production = unit_productions.pop()
            glc[nt].remove(production)
            glc[nt] += glc[production]
            unit_productions += [p for p in glc[production] if len(p) == 1 and p.isupper()]

    # Passo 3: Introduzir variáveis auxiliares
    i = 0  # Índice para as novas variáveis auxiliares
    nonterminals = list(glc.keys())  # Atualizar a lista de não terminais
    for nt in nonterminals:
        productions = glc[nt]  # Produções do não terminal
        new_productions = []
        for production in productions:
            if len(production) > 2:
                new_nt = 'X' + str(i)  # Nova variável auxiliar
                i += 1
                new_productions.append(production[0] + new_nt)
                for j in range(1, len(production) - 1):
                    glc[new_nt] = [production[j] + 'X' + str(i)]
                    i += 1
                    new_nt = 'X' + str(i)  # Nova variável auxiliar
                    i += 1
                new_productions.append(production[-2] + production[-1])
            else:
                new_productions.append(production)
        glc[nt] = new_productions

    # Passo 4: Converter para FNG
    nonterminals = list(glc.keys())  # Atualizar a lista de não terminais
    for nt in nonterminals:
        productions = glc[nt]  # Produções do não terminal
        for production in productions:
            if len(production) > 1 and production[0].islower():
                new_nt = 'X' + str(i)  # Nova variável auxiliar
                i += 1
                glc[new_nt] = [production[1:]]
                glc[nt] = [production[0] + new_nt]

    # Construir a lista de produções na FNG
    for nt, productions in glc.items():
        for production in productions:
            greibach.append(nt + ' -> ' + production)

    return greibach


# Exemplo de uso
glc = {
    'S': ['AB', 'BCS'],
    'A': ['aA', 'C'],
    'B': ['bbB', 'b'],
    'C': ['cC', 'λ']
}

fng = transform_to_greibach(glc)
for production in fng:
    print(production)

