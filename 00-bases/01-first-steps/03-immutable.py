# ¿Qué es inmutabilidad? Significa que algo no puede ser cambiado

nombre = "Ricardo"
# nombre = "Luis" #Valido, el valor si puede ser sustituido, sobreescrito la variable
nombre[0] = "L"
# TypeError: 'str' object does not support item assignment. El valor no puede ser cambiado (mutado). Los strings son inmnutables
print(nombre)
