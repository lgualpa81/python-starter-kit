class Person:
    species = "Humano"

    def __init__(self, name, age):
        self.name = name  # atributos de instancia
        self.age = age

    def work(self):
        return f"{self.name} está trabajando muy duro"

    def eat(self, food):
        if food.lower() == 'tacos':
            return "SUPERPOWERS"
        else:
            return "+Energía"


person1 = Person('Ricardo', 29)
print(person1.name)  # Ricardo
print(person1.age)  # 29
print(person1.species)  # Humano
print(person1.work())  # Ricardo esta trabajando muy duro
print(person1.eat('tacos'))  # SUPERPOWERS
