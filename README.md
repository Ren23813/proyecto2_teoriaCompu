# Conversión de Gramática a CNF y Análisis Sintáctico con CYK

### Autores:
- Renato Rojas
- Melisa Mendizábal


## Descripción
Este proyecto implementa dos componentes fundamentales del análisis sintáctico formal en lenguajes libres de contexto:
- Conversión de una gramática libre de contexto (CFG) a su Forma Normal de Chomsky (CNF).
- Implementación del algoritmo CYK (Cocke–Younger–Kasami) para determinar si una cadena pertenece al lenguaje generado por una gramática dada.
Además, el programa permite generar el árbol de derivación correspondiente a una cadena aceptada.


## Algoritmos Implementados
1. Conversión a Forma Normal de Chomsky (CNF)
   El proceso sigue los pasos clásicos:
   - Añadir un nuevo símbolo inicial.
   - Eliminar producciones ε.
   - Eliminar producciones unitarias.
   - Eliminar símbolos no productivos y no alcanzables.
   - Sustituir terminales en producciones largas.
   - Binarizar las reglas.

2. Algoritmo CYK
  - Utiliza programación dinámica.
  - Crea una tabla triangular que almacena los no terminales que pueden generar cada subcadena.
  - Determina si el símbolo inicial (So) puede generar toda la cadena.


Para interactuar con el programa, se debe ejecutar el main.py. Ahí, se le pedirá ingresar una cadena para verificar su aceptación dentro del lenguaje. Como salida, se obtendrá un mensaje de aceptación o rechazo a la cadena, si esta es aceptada también se mostrará un árbol de la derivación de la cadena.


## Requisitos
Python 3.8 o superior
