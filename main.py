import json
from parte1 import chomsky
from parte2 import CYK, build_tree, tree_to_string
import time

#entrada 
with open("gramatica.json", "r") as archivo: #Para probar cualquier otra gramática, cargarla en "gramatica2.json", con la estructura ya definida y cambiar esta línea (solo agregarle el 2)
    gramaticaOriginal = json.load(archivo)
#Se utiliza el '?' como épsilon al cargar la gramática

variables = gramaticaOriginal['variables']
terminales = gramaticaOriginal['terminales']
simboloInicial = gramaticaOriginal['simboloInicial']
producciones = gramaticaOriginal['producciones']

variablesC, terminalesC, simboloInicialC, produccionesC = chomsky(variables, terminales, simboloInicial, producciones)

menu = 0
print("Bienvenido")
print("Melisa Mendizabal - Renato Rojas")
while menu != '2':
    print('')
    print("1. Comprobar si una cadena está en la gramática")
    print("2. Salir")
    menu = input("Seleccione una opción: ")

    if menu == '1':

        w = input("Ingrese una cadena: ")
        cadena = w.split() #La cadena vacía ingresarla vacía (solo un enter en el input)
        if len(cadena) == 0:
            chronoStart = time.perf_counter()
            eps_present = any(len(rhs) == 0 for rhs in produccionesC.get(simboloInicialC, []))
            aceptado = eps_present
            chronoEnd = time.perf_counter()
        else:
            chronoStart = time.perf_counter()
            aceptado, tabla, back = CYK(produccionesC, cadena)
            chronoEnd = time.perf_counter()
        print("Cadena (partida):",cadena)
        print("¿Cadena aceptada?:", aceptado)
        print("Tiempo tomado para la verificación:", chronoEnd-chronoStart)
        if aceptado:
            if len(cadena) == 0:
                tree = (simboloInicialC, '?')
            else:
                # árbol
                tree = build_tree(back, cadena, simboloInicialC, 0, len(cadena) - 1)
            print("Árbol:")
            print(tree_to_string(tree))
        else:
            print("No hay árbol porque no fue aceptada.")
    
    elif menu == "2":
        print("Gracias por utilizar el programa.")
    
    else: 
        print("Seleccione una opción válida.")

#PRUEBAS
# funcionales = "she cuts".split()       #"he drinks the juice".split() ##"the dog cuts with the knife".split()  ### "she drinks a beer".split() ####"the cat cuts the meat with a spoon".split()
# no_funcionales = "the dog eats cake".split() #"cat in the oven".split() ##"he drinks juice".split() ###

#nonsense = "she cooks a fork".split() #the dog drinks the knife 
