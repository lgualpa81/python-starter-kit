"""
Python no tiene una palabra clave interface, pero puedes usar clases abstractas (ABC) para definir contratos que otras clases deben cumplir.

Además, gracias a su naturaleza dinámica y basada en "duck typing", no necesitas definir interfaces de forma obligatoria como en Java o C#
"""

from abc import ABC, abstractmethod

# Clase abstracta


class Animal(ABC):  # Esta clase actúa como una interfaz

    @abstractmethod
    def sound(self):
        pass

    @abstractmethod
    def sleep(self):
        pass

# Ahora, cualquier clase que herede de Animal deberá implementar ambos métodos para poder ser instanciada:


class Dog(Animal):
    def sound(self):
        return "Woof! Woof!"

    def sleep(self):
        return "zzz.."


class Cat(Animal):
    def sound(self):
        return "Meow! Meow!"

    def sleep(self):
        return "zzz.."


class IncompleteDog(Animal):
    def sound(self):
        print("Guau")

# Esto dará error al intentar instanciar:
# TypeError: Can't instantiate abstract class IncompleteDog...


taquito = Dog()
michifus = Cat()

print(taquito.sound())
print(taquito.sleep())
print(michifus.sound())
print(michifus.sleep())
