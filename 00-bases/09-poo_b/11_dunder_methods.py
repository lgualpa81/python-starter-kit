
# dunder (abreviatura de "double underscore methods")
# son métodos especiales que comienzan y terminan con dos guiones bajos,
# como __init__, __str__, __len__, etc.

"""
Se usan para definir cómo debe comportarse tu objeto cuando interactúa con las funciones y operadores integrados de Python.
Método	      Se activa cuando...	  Ejemplo / Uso
__init__	    Creas una instancia (constructor)	  obj = MiClase()
__str__	      Llamas str(obj) o print(obj)	Personaliza impresión del objeto
__repr__	    Llamas repr(obj) o en la consola	  Representación técnica / debug
__len__	      Llamas len(obj)	  Devuelve el tamaño del objeto
__getitem__	  Accedes con índices: obj[i]	Hace que el objeto sea indexable
__setitem__	  Asignas con índices: obj[i] = valor	Permite modificar elementos indexados
__add__	      Usas + con objetos	Suma personalizada
__call__	    Llamas al objeto como una función	obj()
__eq__	      Comparas: obj1 == obj2	Personaliza igualdad
__lt__, __gt__, etc.	Comparaciones <, >, etc.	Comparaciones personalizadas
__enter__ / __exit__	Usado en with	Para manejo de contexto (archivos, etc.)
"""


class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Hola soy {self.name}"

    def __len__(self):
        return len(self.name)


persona = Person("Ricardo")
print(persona)
print(len(persona))
