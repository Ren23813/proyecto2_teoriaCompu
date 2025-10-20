import json
from parte1 import chomsky
from parte2 import CYK, build_tree, tree_to_string
import time

#entrada (parte 1)
with open("gramatica.json", "r") as archivo:
    gramaticaOriginal = json.load(archivo)

variables = gramaticaOriginal['variables']
terminales = gramaticaOriginal['terminales']
simboloInicial = gramaticaOriginal['simboloInicial']
producciones = gramaticaOriginal['producciones']

variablesC, terminalesC, simboloInicialC, produccionesC = chomsky(variables, terminales, simboloInicial, producciones)

#Parte 2
cadena = "the cat drinks the beer".split()
# cadena = input().split()
chronoStart = time.perf_counter()
aceptado, tabla, back = CYK(produccionesC, cadena)
chronoEnd = time.perf_counter()
print("Cadena (partida):",cadena)
print("¿Cadena aceptada?:", aceptado)
print("Tiempo tomado para la verificación:", chronoEnd-chronoStart)
if aceptado:
    # árbol
    tree = build_tree(back, cadena, "So", 0, len(cadena) - 1)
    print("Árbol:")
    print(tree_to_string(tree))
else:
    print("No hay árbol porque no fue aceptada.")

#PRUEBAS
# funcionales = "she cuts".split()       #"he drinks the juice".split() ##"the dog cuts with the knife".split()  ### "she drinks a beer".split() ####"the cat cuts the meat with a spoon".split()
# no_funcionales = "the dog eats cake".split() #"cat in the oven".split() ##"he drinks juice".split() ###

#nonsense = "she cooks a fork".split()
