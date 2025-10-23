
# == Equal o igualdad

# print(5 == 5) # True
# print(True == 1) # True
# print('' == 1) # False
# print([] == 1) # False
# print(10 == 10.0) # True
# print(10 == 10.1) # False

new_list = []
other_list = []

# is compara en memoria 0x1234ab

# False, porque estan en distintas instancias de memoria
print(new_list is other_list)
print(new_list == other_list)  # True

all([True, 1, {3}])  # True, todos son verdaderos
all([True, 1, {}])  # False, {} is falso
any([True, 1, {}])  # True, True is verdadero
all([])  # True, no hay elementos falsos en la lista
any([])  # False, no hay elementos verdaderos en la lista
