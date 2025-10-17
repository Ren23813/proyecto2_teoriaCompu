

def chomsky(variables, terminales, simboloInicial, producciones):
    nVariables = variables.copy()
    nSimboloInicial = 'So'
    nProducciones = producciones.copy()

    #Añadir nuevo simbolo inicial
    nVariables.append(nSimboloInicial)
    nProducciones[nSimboloInicial] = [[simboloInicial]]

    #Eliminar producciones epsilon: no hay

    #una lista con nuevos estados
    estadosF = []

    #Crear un nuevos estados para los simbolos terminales
    #Recorrer los estados terminales y por cada uno hacer:
    for terminal in terminales:
        #Escribir la misma palabra en Mayusculas
        nuevoEstado = terminal.upper()
        estadosF.append(nuevoEstado)

        #Reemplazar en donde aparezca el terminal
        #Recorrer todas las producciones
        for e in nProducciones:
            produccion = nProducciones[e]

            for p in produccion:

                if p[0] == terminal:
                    #encontrar el indice en la lista del elemento que coincide
                    i = produccion.index([terminal])
                    
                    #eliminar el estado terminal por su indice
                    nProducciones[e].pop(i)

                    #Añadir el nuevo estado
                    nProducciones[e].append([terminal.upper()])

        #Agregar las nuevas producciones (este depues para no ser reemplazadas)
        nProducciones[nuevoEstado] = [[terminal]]

    #Unir ambas listas para unir los estados no trminales
    nVariables.extend(estadosF)
    

    #Binarización
    nuevasProducciones = {}
    contador = 1

    for p in nProducciones:
        nuevasProducciones[p] = []
        for f in nProducciones[p]:
            if len(f) > 2:
                # Vamos a crear reglas intermedias
                simbolos = f[:]  # copia
                cabeza = p
                while len(simbolos) > 2:
                    nuevoVar = f"X{contador}"
                    contador += 1
                    nVariables.append(nuevoVar)

                    # Crear la producción cabeza → primer, nuevoVar
                    nuevasProducciones[cabeza].append([simbolos[0], nuevoVar])

                    # Actualizar: el nuevoVar genera el resto de la cadena
                    simbolos.pop(0)
                    nuevasProducciones[nuevoVar] = [[simbolos[0], simbolos[1]]] if len(simbolos) == 2 else [[simbolos[0], f"X{contador}"]]
                    
                    # Preparar para siguiente iteración
                    cabeza = nuevoVar
                    simbolos.pop(0)
                # ya manejado dentro del bucle
            else:
                nuevasProducciones[p].append(f)

    nProducciones = nuevasProducciones

    #Eliminar las units
    for p in nProducciones:
     
        for f in nProducciones[p]:
            #si es una unit
            if len(f) == 1:
                #se verifica que sea no terminal
                if f[0].isupper():
                    #obtener el valor al que direcciona
                    valorT = nProducciones.get(f[0])

                    #buscar la posición del elemento 
                    i = nProducciones[p].index([f[0]])

                    #reemplazar con el estado terminal correspondiente
                    nProducciones[p][i] = valorT[0]


    nuevasVariables = nVariables.copy()

    #Eliminar de las producciones que no son usadas
    for p in nVariables:
        #contador para ver si el estado es llamado al menos una vez
        if p != nSimboloInicial:
            contador = 0
            for a in nProducciones:
                for f in nProducciones[a]:
                    for i in f:
                        if i == p:
                            contador += 1

        #si no encuentran nada, eliminar el estado de las variables y de las transiciones
        if contador == 0:
            nuevasVariables.remove(p)
            nProducciones.pop(p)
  
                
    return(nuevasVariables, terminales, nSimboloInicial, nProducciones)
    
