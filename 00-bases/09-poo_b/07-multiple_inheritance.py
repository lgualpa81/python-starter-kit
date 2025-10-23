
class Flyer:
    def fly(self):
        print("Puedo volar")

    def do_something(self):
        print("FlyFly")


class Swimmer:
    def swim(self):
        print("Puedo nadar")

    def do_something(self):
        print("SwimSwim")


class Duck(Flyer, Swimmer):
    def quack(self):
        print("Quack!")


donald = Duck()
donald.fly()  # Puedo volar
donald.swim()  # Puedo nadar
donald.quack()  # Quack!
donald.do_something()  # FlyFly


# MRO (Method Resolution Order)
print(Duck.__mro__)
# (<class '__main__.Duck'>, <class '__main__.Flyer'>, <class '__main__.Swimmer'>, <class 'object'>)
