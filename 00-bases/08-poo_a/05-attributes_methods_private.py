class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__password = "1234"  # name mangling _NOMBRECLASE__password
        # _Person__password

    def __generate_password(self):
        return f"$${self.name}{self.age}"


# Por convencion atributos y metodos protegidos inicia con __, no es posible invocarlos
person1 = Person('Ricardo', 29)
print(person1.name)
# Lanza excepcion AttributeError: 'Person' object has no attribute '__password'
print(person1.__password)
# print(person1.__generate_password())
