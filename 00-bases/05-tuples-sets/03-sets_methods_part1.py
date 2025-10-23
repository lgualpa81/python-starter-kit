
# Conjuntos

# .add(), Add an element to a set.
my_set = {1, 2, 3}
my_set.add(6)
my_set.add(3)
my_set.add(5)
print(my_set)  # {1, 2, 3, 5, 6}

# .remove() Elimina un elemento, pero da error sino existe
my_set.remove(2)
my_set.remove(6)
print(my_set)  # {1, 3, 5}

# .discard() No marca error si no existe
my_set.discard(3)
my_set.discard(3)
my_set.discard(7)

print(my_set)  # {1, 5}

# .pop() Elimina un elemento al azar y lo devuelve

print(my_set.pop())  # 1
print(my_set)  # {5}
