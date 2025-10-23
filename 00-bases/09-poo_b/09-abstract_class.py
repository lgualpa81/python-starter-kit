
from abc import ABC, abstractmethod

# Clase abstracta


class Animal(ABC):

    @abstractmethod
    def sound(self):
        pass

    def sleep(self):
        print("zzzz....")


class Dog(Animal):
    def sound(self):
        print("Woof!")


# animal = Animal()  # genera error
# TypeError: Can't instantiate abstract class Animal without an implementation for abstract method 'sound'

dog = Dog()
dog.sound()  # Woof!
dog.sleep()  # zzzz....

"""
No puedes instanciar una clase abstracta si tiene métodos abstractos sin implementar.

Debes crear una subclase concreta que implemente todos los métodos abstractos.

Solo entonces podrás crear instancias de esa subclase.
"""
