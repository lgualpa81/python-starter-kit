
class Person:
    def __init__(self, name, age):
        if (age > 18):
            self.name = name
            self.age = age


person1 = Person('Ricardo', 29)

print(person1)  # <__main__.Person object at 0x7377d3acc650>
print(person1.name)  # Ricardo
print(person1.age)  # 29

person2 = Person('Fernando', 10)
print(person2)  # <__main__.Person object at 0x7377d3acc710>
# Lanza exception porque self.name no ha sido instanciado.
# (AttributeError: 'Person' object has no attribute 'name')
print(person2.name)
print(person2.age)
