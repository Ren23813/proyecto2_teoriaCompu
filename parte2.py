def CYK(Cproducciones, w):
    n = len(w)
    tabla = [[set() for j in range(n)] for i in range(n)]

    for j in range(n):
        for A, reglas in Cproducciones.items():
            for regla in reglas:
                if len(regla) == 1 and regla[0] == w[j]:
                    tabla[j][j].add(A)

    for longitud in range(2, n + 1):      
        for i in range(n - longitud + 1): 
            j = i + longitud - 1          
            for k in range(i, j):         
                for A, reglas in Cproducciones.items():
                    for regla in reglas:
                        if len(regla) == 2:
                            B, C = regla
                            if B in tabla[i][k] and C in tabla[k + 1][j]:
                                tabla[i][j].add(A)

    aceptado = "So" in tabla[0][n - 1]

    return aceptado, tabla
