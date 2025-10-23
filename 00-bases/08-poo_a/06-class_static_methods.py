
class Person:
    species = "Humano"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def change_species(cls, new_specie):
        cls.species = new_specie

    @staticmethod
    def is_older(age):
        return age >= 18


person1 = Person("Ricardo", 29)
print(person1.species)  # Humano
Person.change_species("Reptilianos")
print(person1.species)  # Reptilianos

person2 = Person("Fernando", 20)
print(person2.species)  # Reptilianos


print(Person.is_older(16))  # False

person1 = Person("Ricardo", 29)
print(person1.is_older(person1.age))  # True
