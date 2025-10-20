def CYK(Cproducciones, w):
    n = len(w)
    tabla = [[set() for j in range(n)] for i in range(n)]
    back = {}  

    for j in range(n):
        for A, reglas in Cproducciones.items():
            for regla in reglas:
                if len(regla) == 1 and regla[0] == w[j]:
                    tabla[j][j].add(A)
                    back.setdefault((j, j, A), []).append(('terminal', j))

    for longitud in range(2, n + 1):
        for i in range(n - longitud + 1):
            j = i + longitud - 1
            for k in range(i, j):
                for A, reglas in Cproducciones.items():
                    for regla in reglas:
                        if len(regla) == 2:
                            B, C = regla
                            if (B in tabla[i][k]) and (C in tabla[k + 1][j]):
                                if A not in tabla[i][j]:
                                    tabla[i][j].add(A)
                                back.setdefault((i, j, A), []).append(('binary', k, B, C))

    aceptado = "So" in tabla[0][n - 1] if n > 0 else False
    return aceptado, tabla, back

def build_tree(back, w, A, i, j):
    key = (i, j, A)
    entradas = back.get(key)
    if not entradas:
        return None

    entrada = entradas[0]  
    if entrada[0] == 'terminal':
        pos = entrada[1]
        return (A, w[pos])
    elif entrada[0] == 'binary':
        _, k, B, C = entrada
        left = build_tree(back, w, B, i, k)
        right = build_tree(back, w, C, k + 1, j)
        return (A, left, right)

def tree_to_string(tree, indent=0):
    if tree is None:
        return " " * indent + "None\n"
    if len(tree) == 2 and isinstance(tree[1], str):
        # hoja (terminal)
        return " " * indent + f"{tree[0]} -> {tree[1]}\n"
    # nodo (no terminal con hijos)
    s = " " * indent + f"{tree[0]}\n"
    for child in tree[1:]:
        s += tree_to_string(child, indent + 2)
    return s
