import json
from parte1 import chomsky


#entrada
with open("gramatica.json", "r") as archivo:
    gramaticaOriginal = json.load(archivo)

variables = gramaticaOriginal['variables']
terminales = gramaticaOriginal['terminales']
simboloInicial = gramaticaOriginal['simboloInicial']
producciones = gramaticaOriginal['producciones']

variablesC, terminalesC, simboloInicialC, produccionesC = chomsky(variables, terminales, simboloInicial, producciones)
print(variablesC)
print(terminalesC)
print(simboloInicialC)
print(produccionesC)

# print(terminales)
# print(simboloInicial)
# print(producciones)
