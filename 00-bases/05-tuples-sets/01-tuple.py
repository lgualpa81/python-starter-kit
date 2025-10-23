
my_tuple = (1, 2, 3, 4, "Hola", True, 2, "Hi", 5, 4, 3, 2)
print(my_tuple)

# Ordenada
# INMUTABLES
# Permite duplicados
# Indexadas

# Métodos
# .count(), Return number of occurrences of value.
print(my_tuple.count(2))

# .index(), Return first index of value.(element, start, stop)
print(my_tuple.index(2))

# my_tuple[4] = "Mundo" # ESTO NO SE PUEDE
new_tuple = my_tuple[4]

print(new_tuple)

week = ('Lunes', 'Martes', 'Miercoles', 'Jueves',
        'Viernes', ' Sabado', 'Domingo')
print(week)
