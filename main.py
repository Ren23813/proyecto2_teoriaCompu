import json
from parte1 import chomsky
from parte2 import CYK

#entrada
with open("gramatica.json", "r") as archivo:
    gramaticaOriginal = json.load(archivo)

variables = gramaticaOriginal['variables']
terminales = gramaticaOriginal['terminales']
simboloInicial = gramaticaOriginal['simboloInicial']
producciones = gramaticaOriginal['producciones']

variablesC, terminalesC, simboloInicialC, produccionesC = chomsky(variables, terminales, simboloInicial, producciones)

cadena = "she cooks a fork".split()
# funcionales = "she cuts".split()       #"he drinks the juice".split() ##"the dog cuts with the knife".split()  ### "she drinks a beer".split() ####"the cat cuts the meat with a spoon".split()
# no_funcionales = "the dog eats cake".split() #"cat in the oven".split() ##"he drinks juice".split() ###
aceptado, tabla = CYK(produccionesC, cadena)


#nonsense = "she cooks a fork".split()
print("¿Cadena aceptada?:", aceptado)
for fila in tabla:
    print(fila)
